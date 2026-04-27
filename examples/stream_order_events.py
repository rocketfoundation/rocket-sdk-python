"""Stream order events for an account via WebSocket.

Subscribes to ``OrderEvents`` for a single account and prints one compact
line per event as it arrives. Press Ctrl+C to stop.

The account to watch is resolved as follows:
  1. ``--address 0x...`` CLI argument, if provided, OR
  2. The address derived from ``ROCKET_PRIVATE_KEY``

``ROCKET_RPC_URL`` is always required (used for the WebSocket connection
and for fetching instrument metadata so the output can show tickers).

Usage:
    python stream_order_events.py
    python stream_order_events.py --address 0xfe0F5544a746dA9BEb8046b10bE24a20659a9D83
"""

import argparse
import asyncio
import datetime
import os
import signal
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from rocket_sdk_python.client.rest import RestClient
from rocket_sdk_python.client.ws import WsClient
from rocket_sdk_python.crypto.signer import AccountSigner
from rocket_sdk_python.types.ws import (
    OrderEventsSubscription,
    OrderEventsSubscriptionFields,
    OrderEventUpdate,
    OrderEventUpdateFields,
    ServerMessage,
    Subscribe,
)

from example_utils import load_env_from_file


def normalize_rpc_url(url: str) -> str:
    """Ensure the RPC URL has an http(s) scheme; default to https."""
    url = url.strip().rstrip("/")
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def resolve_account_and_rpc(address_arg: str | None) -> tuple[str, str]:
    load_env_from_file()

    rpc_url = os.environ.get("ROCKET_RPC_URL")
    if not rpc_url:
        print("Error: ROCKET_RPC_URL not set in environment or .env file")
        sys.exit(1)
    rpc_url = normalize_rpc_url(rpc_url)

    if address_arg:
        addr = address_arg.lower()
        if not addr.startswith("0x") or len(addr) != 42:
            print(f"Error: --address must be a 0x-prefixed 20-byte hex address, got {address_arg!r}")
            sys.exit(1)
        return address_arg, rpc_url

    private_key = os.environ.get("ROCKET_PRIVATE_KEY")
    if not private_key:
        print("Error: pass --address or set ROCKET_PRIVATE_KEY in environment / .env")
        sys.exit(1)
    if not private_key.startswith("0x"):
        private_key = "0x" + private_key

    signer = AccountSigner.from_private_key(private_key)
    return str(signer.address), rpc_url


def fetch_ticker_map(rpc_url: str) -> dict[str, str]:
    """Map instrument id (as str) -> ticker. Empty on failure."""
    try:
        with RestClient(rpc_url) as client:
            resp = client.get_instruments()
            return {str(iid): inst.ticker for iid, inst in resp.instruments.root.items()}
    except Exception as e:
        print(f"Warning: could not fetch instruments for ticker labels: {e}")
        return {}


def make_handler(account: str, tickers: dict[str, str]):
    short_addr = f"{account[:6]}…{account[-4:]}"

    def instr_label(instrument: str) -> str:
        ticker = tickers.get(str(instrument))
        return ticker if ticker else str(instrument)

    def handle_message(msg: ServerMessage):
        ts = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]

        if isinstance(msg, (OrderEventUpdate, OrderEventUpdateFields)):
            update = msg.OrderEventUpdate if isinstance(msg, OrderEventUpdate) else msg
            for ev in update.order_events:
                line = format_event(ev, ts, instr_label)
                print(line)
            return

        if hasattr(msg, "SubscribeConfirmation"):
            print(f"[{ts}]  subscribed: OrderEvents account={short_addr}")
            return

        if hasattr(msg, "Error"):
            print(f"[{ts}]  error: {msg.Error}")

    return handle_message


def format_event(ev, ts: str, instr_label) -> str:
    instr = instr_label(ev.instrument)
    base = f"[{ts}]  order={ev.order_id}  {instr:<20}"
    data = ev.event_data

    if hasattr(data, "placed"):
        p = data.placed
        return (
            f"{base}  PLACED      "
            f"price={p.price}  size={p.size}  "
            f"remaining={p.remaining_size}  passive={p.is_passive}"
        )

    if hasattr(data, "fill"):
        f = data.fill
        pnl = f"  pnl={f.pnl}" if f.pnl is not None else ""
        flags = []
        if f.is_filled:
            flags.append("filled")
        if f.is_passive:
            flags.append("passive")
        if f.is_liquidation:
            flags.append("liquidation")
        if f.is_adl:
            flags.append("adl")
        flags_str = f"  [{','.join(flags)}]" if flags else ""
        return (
            f"{base}  FILL        "
            f"price={f.price}  size={f.size}  remaining={f.remaining_size}  "
            f"fee={f.fee_amount}@{f.fee_rate}{pnl}{flags_str}"
        )

    if hasattr(data, "modified"):
        m = data.modified
        return f"{base}  MODIFIED    price={m.price}  size={m.size}"

    if hasattr(data, "rejected"):
        return f"{base}  REJECTED    reason={data.rejected.reason}"

    if hasattr(data, "root") and data.root == "canceled":
        return f"{base}  CANCELED"

    return f"{base}  UNKNOWN     {data!r}"


async def main():
    parser = argparse.ArgumentParser(description="Stream simplified order events for an account.")
    parser.add_argument(
        "--address",
        help="Account address to watch (defaults to address derived from ROCKET_PRIVATE_KEY)",
    )
    args = parser.parse_args()

    account, rpc_url = resolve_account_and_rpc(args.address)
    ws_url = rpc_url.replace("https://", "wss://").replace("http://", "ws://") + "/ws"

    print(f"Watching account: {account}")
    print(f"Connecting to:    {ws_url}")

    tickers = fetch_ticker_map(rpc_url)
    if tickers:
        print(f"Loaded {len(tickers)} instrument ticker(s).")

    client = WsClient(ws_url, make_handler(account, tickers))
    client_task = asyncio.create_task(client.connect())

    await asyncio.sleep(1)

    await client._send_queue.put(
        Subscribe(
            Subscribe=OrderEventsSubscription(
                OrderEvents=OrderEventsSubscriptionFields(account=account)
            )
        )
    )

    print(f"\n{'=' * 64}")
    print("Streaming order events  —  Ctrl+C to stop")
    print(f"{'=' * 64}\n")

    shutdown = asyncio.Event()

    def on_signal(sig, frame):
        shutdown.set()

    signal.signal(signal.SIGINT, on_signal)
    signal.signal(signal.SIGTERM, on_signal)

    try:
        await shutdown.wait()
    except KeyboardInterrupt:
        pass

    print("\nShutting down ...")
    await client.close()
    await client_task
    print("Done.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExited.")

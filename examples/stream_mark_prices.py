"""Stream mark prices for all instruments via WebSocket.

Subscribes to the PriceFeed for every listed instrument and prints each
mark-price update as it arrives.  Press Ctrl+C to stop.

Usage:
    ROCKET_PRIVATE_KEY=0x... ROCKET_RPC_URL=https://... python stream_mark_prices.py

Or put the variables in a .env file next to the script.
"""

import asyncio
import datetime
import os
import signal
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from rocket_sdk_python.client.ws import WsClient
from rocket_sdk_python.sdk import RocketSDK
from rocket_sdk_python.types.ws import (
    PriceFeedSubscription,
    PriceFeedSubscriptionFields,
    ServerMessage,
    Subscribe,
)

from example_utils import get_credentials


def handle_message(msg: ServerMessage):
    ts = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]

    if hasattr(msg, "MarkPriceUpdate"):
        update = msg.MarkPriceUpdate
        pd = update.mark_price.Price
        iv_str = f"  iv={pd.iv}" if pd.iv is not None else ""
        print(f"[{ts}]  instrument={update.instrument_id}  "
              f"price={pd.price}  timestamp={pd.timestamp}{iv_str}")

    elif hasattr(msg, "SubscribeConfirmation"):
        print(f"[{ts}]  subscribed: {msg.SubscribeConfirmation}")

    elif hasattr(msg, "Error"):
        print(f"[{ts}]  error: {msg.Error}")


async def main():
    private_key, rpc_url = get_credentials()

    sdk = RocketSDK(private_key, rpc_url)
    ws_url = rpc_url.replace("https://", "wss://").replace("http://", "ws://") + "/ws"

    print(f"Connecting to {ws_url} ...")
    client = WsClient(ws_url, handle_message)
    client_task = asyncio.create_task(client.connect())

    await asyncio.sleep(2)

    instruments = sdk._client.get_instruments().instruments.root
    if not instruments:
        print("No instruments found.")
        await client.close()
        await client_task
        sdk.close()
        return

    print(f"Subscribing to mark prices for {len(instruments)} instrument(s):\n")
    for iid, inst in instruments.items():
        print(f"  {inst.ticker} (id={iid})")
        await client._send_queue.put(
            Subscribe(
                Subscribe=PriceFeedSubscription(
                    PriceFeed=PriceFeedSubscriptionFields(instrument_id=iid)
                )
            )
        )

    print(f"\n{'=' * 64}")
    print("Streaming mark prices  —  Ctrl+C to stop")
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
    sdk.close()
    print("Done.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExited.")

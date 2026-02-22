import asyncio
import json
import signal
import sys

sys.path.insert(0, "../src")

from rocket_sdk_python.client.ws import WsClient
from rocket_sdk_python.sdk import RocketSDK
from rocket_sdk_python.types.ws import (
    CollateralSubscription,
    CollateralSubscriptionFields,
    InstrumentStatsSubscription,
    InstrumentStatsSubscriptionFields,
    OpenOrdersSubscription,
    OpenOrdersSubscriptionFields,
    OrderbookSubscription,
    OrderbookSubscriptionFields,
    OrderEventsSubscription,
    OrderEventsSubscriptionFields,
    PositionSubscription,
    PositionSubscriptionFields,
    PriceFeedSubscription,
    PriceFeedSubscriptionFields,
    ServerMessage,
    Subscribe,
)

from example_utils import get_credentials


def handle_message(msg: ServerMessage):
    import datetime
    timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]

    print(f"\n{'='*80}")
    print(f"SERVER MESSAGE [{timestamp}]:")
    print(f"{'='*80}")

    if hasattr(msg, "OrderEventUpdate"):
        print(f"📦 TYPE: OrderEventUpdate")
        update = msg.OrderEventUpdate
        print(f"Account: {update.account}")
        print(f"Instrument ID: {update.instrument_id}")
        print(f"Number of events: {len(update.order_events)}")

        for i, event in enumerate(update.order_events, 1):
            print(f"\n  Event #{i}:")
            print(f"    Order ID: {event.order_id}")
            print(f"    Order IX: {event.order_ix}")
            print(f"    Account: {event.account}")
            print(f"    Instrument: {event.instrument}")

            if event.event_data.type == "Placed":
                print(f"    ✓ EVENT: PLACED")
                print(f"      Price: {event.event_data.price}")
                print(f"      Size: {event.event_data.size}")
                print(f"      Remaining Size: {event.event_data.remaining_size}")
                print(f"      Original Size: {event.event_data.original_size}")
                print(f"      Settlement Asset: {event.event_data.settlement_asset}")
                print(f"      Is Passive: {event.event_data.is_passive}")
                print(f"      Is Filled: {event.event_data.is_filled}")

            elif event.event_data.type == "Fill":
                print(f"    ✓ EVENT: FILL")
                print(f"      Price: {event.event_data.price}")
                print(f"      Size: {event.event_data.size}")
                print(f"      Remaining Size: {event.event_data.remaining_size}")
                print(f"      Original Size: {event.event_data.original_size}")
                print(f"      Settlement Asset: {event.event_data.settlement_asset}")
                print(f"      Fee Rate: {event.event_data.fee_rate}")
                print(f"      Fee Amount: {event.event_data.fee_amount}")
                print(f"      PnL: {event.event_data.pnl}")
                print(f"      Is Passive: {event.event_data.is_passive}")
                print(f"      Is Filled: {event.event_data.is_filled}")
                print(f"      Is Liquidation: {event.event_data.is_liquidation}")

            elif event.event_data.type == "Rejected":
                print(f"    ✗✗✗ EVENT: REJECTED ✗✗✗")
                print(f"      🚨 REJECTION REASON: {event.event_data.reason}")
                print(f"      Order ID: {event.order_id}")
                print(f"      Instrument: {event.instrument}")

            elif event.event_data.type == "Cancelled":
                print(f"    ⊘ EVENT: CANCELLED")

            elif event.event_data.type == "Modified":
                print(f"    ⚙ EVENT: MODIFIED")
                print(f"      Price: {event.event_data.price}")
                print(f"      Size: {event.event_data.size}")

            else:
                print(f"    ⚠️  UNKNOWN EVENT TYPE: {event.event_data.type}")
                print(f"      Raw event data: {event.event_data.model_dump_json(by_alias=True, indent=6)}")

    elif hasattr(msg, "OpenOrdersUpdate"):
        print(f"📋 TYPE: OpenOrdersUpdate")
        update = msg.OpenOrdersUpdate
        print(f"Account: {update.account}")
        print(f"Number of orders: {len(update.orders)}")

        for i, order in enumerate(update.orders, 1):
            print(f"\n  Order #{i}:")
            print(f"    Order ID: {order.order_id}")
            print(f"    Side: {order.side}")
            print(f"    Price: {order.price}")
            print(f"    Quantity: {order.quantity}")

    elif hasattr(msg, "CollateralUpdate"):
        print(f"💰 TYPE: CollateralUpdate")
        update = msg.CollateralUpdate
        asset_name = {0: "USDC", 1: "BTC", 2: "ETH"}.get(update.asset_id, f"Asset {update.asset_id}")
        print(f"Account: {update.account}")
        print(f"Asset: {asset_name} (ID {update.asset_id})")
        print(f"Collateral: {update.collateral}")

    elif hasattr(msg, "PositionUpdate"):
        print(f"📊 TYPE: PositionUpdate")
        update = msg.PositionUpdate
        print(f"Account: {update.account}")
        print(f"Positions: {json.dumps(update.positions.model_dump(by_alias=True), indent=2)}")

    elif hasattr(msg, "QuoteUpdate"):
        print(f"📈 TYPE: QuoteUpdate (Orderbook)")
        update = msg.QuoteUpdate
        print(f"Instrument ID: {update.instrument_id}")
        print(f"Best bid: {update.quote.best_bid}")
        print(f"Best ask: {update.quote.best_ask}")

    elif hasattr(msg, "MarkPriceUpdate"):
        print(f"💹 TYPE: MarkPriceUpdate (PriceFeed)")
        update = msg.MarkPriceUpdate
        print(f"Instrument ID: {update.instrument_id}")
        print(f"Mark price: {update.mark_price}")

    elif hasattr(msg, "InstrumentStatsUpdate"):
        print(f"📊 TYPE: InstrumentStatsUpdate")
        update = msg.InstrumentStatsUpdate
        print(f"Instrument ID: {update.instrument_id}")
        print(f"Stats: {json.dumps(update.stats.model_dump(by_alias=True), indent=2)}")

    elif hasattr(msg, "SubscribeConfirmation"):
        print(f"✓ TYPE: SubscribeConfirmation")

    elif hasattr(msg, "Error"):
        print(f"❌ TYPE: Error")
        print(f"Message: {msg.Error}")

    else:
        print(f"📨 TYPE: {type(msg).__name__}")
        print(f"Raw message: {msg.model_dump_json(by_alias=True, indent=2)}")

    print(f"{'='*80}\n")


async def main():
    private_key, rpc_url = get_credentials()

    sdk = RocketSDK(private_key, rpc_url)
    print(f"Account address: {sdk.address}\n")

    ws_url = rpc_url.replace("https://", "wss://").replace("http://", "ws://") + "/ws"
    print(f"Connecting to WebSocket: {ws_url}\n")

    client = WsClient(ws_url, handle_message)

    async def run_client():
        await client.connect()

    client_task = asyncio.create_task(run_client())

    await asyncio.sleep(2)

    print("Fetching instruments...")
    instruments_response = sdk._client.get_instruments()
    instruments = instruments_response.instruments.root

    if not instruments:
        print("No instruments available!")
        await client.close()
        await client_task
        sdk.close()
        return

    instrument_id = next(
            (k for k, v in instruments.items() if v.ticker == "PERP_ETH_USDC"),
            None
        )
    instrument = instruments[instrument_id]
    print(f"Using instrument: {instrument.ticker} (ID: {instrument.id})\n")

    print("Subscribing to feeds...")

    # print("  - Orderbook (QuoteUpdate)")
    # await client._send_queue.put(
    #     Subscribe(
    #         Subscribe=OrderbookSubscription(
    #             Orderbook=OrderbookSubscriptionFields(instrument_id=instrument_id)
    #         )
    #     )
    # )

    # print("  - PriceFeed (MarkPriceUpdate)")
    # await client._send_queue.put(
    #     Subscribe(
    #         Subscribe=PriceFeedSubscription(
    #             PriceFeed=PriceFeedSubscriptionFields(instrument_id=instrument_id)
    #         )
    #     )
    # )

    # print("  - InstrumentStats")
    # await client._send_queue.put(
    #     Subscribe(
    #         Subscribe=InstrumentStatsSubscription(
    #             InstrumentStats=InstrumentStatsSubscriptionFields(instrument_id=instrument_id)
    #         )
    #     )
    # )

    print("  - OrderEvents (your account)")
    await client._send_queue.put(
        Subscribe(
            Subscribe=OrderEventsSubscription(
                OrderEvents=OrderEventsSubscriptionFields(account=sdk.address)
            )
        )
    )

    print("  - OpenOrders (your account)")
    await client._send_queue.put(
        Subscribe(
            Subscribe=OpenOrdersSubscription(
                OpenOrders=OpenOrdersSubscriptionFields(account=sdk.address)
            )
        )
    )

    # print("  - Position (your account)")
    # await client._send_queue.put(
    #     Subscribe(
    #         Subscribe=PositionSubscription(
    #             Position=PositionSubscriptionFields(
    #                 account=sdk.address,
    #                 instrument_id=instrument_id
    #             )
    #         )
    #     )
    # )

    print("  - Collateral (USDC)")
    await client._send_queue.put(
        Subscribe(
            Subscribe=CollateralSubscription(
                Collateral=CollateralSubscriptionFields(asset_id=0, account=sdk.address)
            )
        )
    )

    print("\n" + "="*80)
    print("LISTENING FOR WEBSOCKET EVENTS")
    print("="*80)
    print("This listener only receives events. It does NOT place orders.")
    print("To see order rejection events, place an order using:")
    print("  - simple_bot.py")
    print("  - websocket_example.py")
    print("  - or the frontend")
    print("\nPress Ctrl+C to stop\n")

    shutdown_event = asyncio.Event()

    def signal_handler(sig, frame):
        print("\n\n⚠️  Received shutdown signal...")
        shutdown_event.set()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        await shutdown_event.wait()
    except KeyboardInterrupt:
        pass

    print("Shutting down gracefully...")
    print("  - Closing WebSocket connection...")
    await client.close()
    print("  - Waiting for client task...")
    await client_task
    print("  - Closing SDK...")
    sdk.close()
    print("✓ Shutdown complete!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n✓ Exited")


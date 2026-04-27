import asyncio
import json
import sys

sys.path.insert(0, "../src")

from rocket_sdk_python.client.ws import WsClient
from rocket_sdk_python.sdk import RocketSDK
from rocket_sdk_python.types.primitives import OrderSide
from rocket_sdk_python.types.ws import (
    OpenOrdersSubscription,
    OpenOrdersSubscriptionFields,
    OrderEventsSubscription,
    OrderEventsSubscriptionFields,
    OrderEventUpdateFields,
    ServerMessage,
    Subscribe,
)

from example_utils import get_credentials


def handle_message(msg: ServerMessage):
    print(f"\n{'=' * 80}")
    print("SERVER MESSAGE:")
    print(f"{'=' * 80}")

    if hasattr(msg, "OrderEventUpdate") or isinstance(msg, OrderEventUpdateFields):
        print("📦 TYPE: OrderEventUpdate")
        update = msg if isinstance(msg, OrderEventUpdateFields) else msg.OrderEventUpdate
        print(f"Account: {update.account}")
        print(f"Instrument ID: {update.instrument_id}")
        print(f"Number of events: {len(update.order_events)}")

        for i, event in enumerate(update.order_events, 1):
            print(f"\n  Event #{i}:")
            print(f"    Order ID: {event.order_id}")
            print(f"    Account: {event.account}")
            print(f"    Instrument: {event.instrument}")

            event_data = event.event_data

            if hasattr(event_data, "placed"):
                placed = event_data.placed
                print("    ✓ EVENT: PLACED")
                print(f"      Price: {placed.price}")
                print(f"      Size: {placed.size}")
                print(f"      Remaining Size: {placed.remaining_size}")
                print(f"      Original Size: {placed.original_size}")
                print(f"      Settlement Asset: {placed.settlement_asset}")
                print(f"      Is Passive: {placed.is_passive}")
                print(f"      Is Filled: {placed.is_filled}")

            elif hasattr(event_data, "fill"):
                fill = event_data.fill
                print("    ✓ EVENT: FILL")
                print(f"      Price: {fill.price}")
                print(f"      Size: {fill.size}")
                print(f"      Remaining Size: {fill.remaining_size}")
                print(f"      Original Size: {fill.original_size}")
                print(f"      Settlement Asset: {fill.settlement_asset}")
                print(f"      Fee Rate: {fill.fee_rate}")
                print(f"      Fee Amount: {fill.fee_amount}")
                print(f"      PnL: {fill.pnl}")
                print(f"      Is Passive: {fill.is_passive}")
                print(f"      Is Filled: {fill.is_filled}")
                print(f"      Is Liquidation: {fill.is_liquidation}")
                print(f"      Is ADL: {fill.is_adl}")

            elif hasattr(event_data, "rejected"):
                print("    ✗ EVENT: REJECTED")
                print(f"      Reason: {event_data.rejected.reason}")

            elif hasattr(event_data, "root") and event_data.root == "canceled":
                print("    ⊘ EVENT: CANCELED")

            elif hasattr(event_data, "modified"):
                modified = event_data.modified
                print("    ⚙ EVENT: MODIFIED")
                print(f"      Price: {modified.price}")
                print(f"      Size: {modified.size}")

    elif hasattr(msg, "OpenOrdersUpdate"):
        print("📋 TYPE: OpenOrdersUpdate")
        update = msg.OpenOrdersUpdate
        print(f"Account: {update.account}")
        print(f"Number of orders: {len(update.orders)}")

        for i, order in enumerate(update.orders, 1):
            print(f"\n  Order #{i}:")
            print(f"    Order ID: {order.order_id}")
            print(f"    Side: {order.side}")
            print(f"    Price: {order.price}")
            print(f"    Quantity: {order.quantity}")
            print(f"    Instrument: {order.instrument}")

    elif hasattr(msg, "CollateralUpdate"):
        print("💰 TYPE: CollateralUpdate")
        update = msg.CollateralUpdate
        print(f"Account: {update.account}")
        print(f"Asset ID: {update.asset_id}")
        print(f"Collateral: {update.collateral}")

    elif hasattr(msg, "PositionUpdate"):
        print("📊 TYPE: PositionUpdate")
        update = msg.PositionUpdate
        print(f"Account: {update.account}")
        print(
            f"Positions: {json.dumps(update.positions.model_dump(by_alias=True), indent=2)}"
        )

    elif hasattr(msg, "SubscribeConfirmation"):
        print("✓ TYPE: SubscribeConfirmation")

    elif hasattr(msg, "UnsubscribeConfirmation"):
        print("✓ TYPE: UnsubscribeConfirmation")

    elif hasattr(msg, "Pong"):
        print("🏓 TYPE: Pong")

    elif hasattr(msg, "Error"):
        print("❌ TYPE: Error")
        print(f"Message: {msg.Error}")

    else:
        print(f"📨 TYPE: {type(msg).__name__}")
        print(f"Raw: {msg.model_dump_json(by_alias=True, indent=2)}")

    print(f"{'=' * 80}\n")


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

    print("Subscribing to order events for your account...")
    await client._send_queue.put(
        Subscribe(
            Subscribe=OrderEventsSubscription(
                OrderEvents=OrderEventsSubscriptionFields(account=sdk.address)
            )
        )
    )

    print("Subscribing to open orders for your account...")
    await client._send_queue.put(
        Subscribe(
            Subscribe=OpenOrdersSubscription(
                OpenOrders=OpenOrdersSubscriptionFields(account=sdk.address)
            )
        )
    )

    print("Subscribing to collateral updates for your account...")
    from rocket_sdk_python.types.ws import (
        CollateralSubscription,
        CollateralSubscriptionFields,
    )

    await client._send_queue.put(
        Subscribe(
            Subscribe=CollateralSubscription(
                Collateral=CollateralSubscriptionFields(asset_id=0, account=sdk.address)
            )
        )
    )

    await asyncio.sleep(2)

    print("\nFetching instruments...")
    instruments_response = sdk._client.get_instruments()
    instruments = instruments_response.instruments.root

    if not instruments:
        print("No instruments available!")
        await client.close()
        await client_task
        sdk.close()
        return

    instrument_id = list(instruments.keys())[0]
    instrument = instruments[instrument_id]
    print(f"Selected instrument: {instrument.ticker} (ID: {instrument.id})")
    print(f"  Last price: {instrument.last_match_price}")

    last_price = float(instrument.last_match_price)
    bid_price = last_price * 0.85
    quantity = 1000

    print(f"\n{'=' * 80}")
    print("PLACING ORDER")
    print(f"{'=' * 80}")
    print(f"Instrument: {instrument.ticker}")
    print("Side: BUY")
    print(f"Last price: {last_price:.2f}")
    print(f"Bid price: {bid_price:.2f} (85% of last)")
    print(f"Quantity: {quantity / instrument.quantity_scale}")
    print(f"{'=' * 80}\n")

    sdk.place_limit_order(
        instrument_id=instrument_id,
        side=OrderSide.BUY,
        price=str(int(bid_price * instrument.price_scale)),
        quantity=str(quantity),
    )

    print("Transaction submitted. Waiting for WebSocket events...\n")

    print("Listening for 30 seconds...")
    print(
        "You should see OrderEventUpdate with either PLACED, FILLED, or REJECTED event\n"
    )

    await asyncio.sleep(30)

    print("\nClosing WebSocket connection...")
    await client.close()
    await client_task

    sdk.close()
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())

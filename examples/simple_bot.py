import sys
import time

sys.path.insert(0, "src")

from example_utils import get_credentials
from rocket_sdk_python import RocketSDK, OrderSide


def main():
    private_key, rpc_url = get_credentials()

    print(f"Connecting to {rpc_url}...")
    with RocketSDK(private_key, rpc_url) as sdk:
        print(f"Account address: {sdk.address}")
        print()

        print("Fetching instruments...")
        instruments_response = sdk._client.get_instruments()
        instruments = instruments_response.instruments.root

        if not instruments:
            print("No instruments available")
            return

        instrument_id = next(
            (k for k, v in instruments.items() if v.ticker == "PERP_ETH_USDC"), None
        )
        instrument = instruments[instrument_id]
        print(f"Selected instrument: {instrument.ticker} (ID: {instrument_id})")
        print(f"  Last price: {instrument.last_match_price}")
        print(f"  Price scale: {instrument.price_scale}")
        print(f"  Quantity scale: {instrument.quantity_scale}")
        print()

        print("Fetching all assets...")
        assets_response = sdk._client.get_assets()
        print(f"Total assets: {len(assets_response.assets.root)}")
        for asset in assets_response.assets.root.values():
            print(f"  Asset ID {asset.id}: {asset.ticker}")
        print()

        print("Fetching account collateral...")
        collateral_response = sdk.get_collateral()
        collaterals = collateral_response.collaterals.root
        print(f"Total collateral entries: {len(collaterals)}")
        print("All collateral balances:")
        for asset_id, balance in collaterals.items():
            print(f"  Asset ID {asset_id}: {balance}")
        print()

        print("Fetching open positions...")
        positions_response = sdk.get_positions()
        if positions_response.positions:
            print(f"Open positions: {len(positions_response.positions.root)}")
            for instrument_id, pos in positions_response.positions.root.items():
                print(
                    f"  Instrument {instrument_id}: quantity={pos.quantity}, average_price={pos.average_price}"
                )
        else:
            print("Open positions: 0")
        print()

        print("Fetching open orders...")
        orders_response = sdk.get_open_orders()
        if orders_response.orders:
            print(f"Open orders: {len(orders_response.orders)}")
            for order in orders_response.orders:
                print(
                    f"  Order {order.order_id}: {order.side} {order.quantity} @ {order.price}"
                )
        else:
            print("Open orders: 0")
        print()

        last_price = float(instrument.last_match_price)
        bid_price = last_price * 0.95
        # bid_price_scaled = str(int(bid_price * instrument.price_scale))

        # quantity = str(1 * instrument.quantity_scale)
        bid_price_scaled = str(bid_price)
        quantity = str(1)

        print(
            f"Placing limit BUY order at {bid_price:.2f} (scaled: {bid_price_scaled})..."
        )
        print(f"  Last price: {last_price:.2f}")
        print(f"  Bid price: {bid_price:.2f} (90% of last)")
        print(f"  Quantity: {quantity}")
        try:
            tx_response = sdk.place_limit_order(
                instrument_id=instrument_id,
                side=OrderSide.BUY,
                price=bid_price_scaled,
                quantity=quantity,
                reduce_only=False,
                take_profit=False,
            )

            print("\n=== FULL TRANSACTION RESPONSE ===")
            print(f"Response type: {tx_response.type}")
            print(f"Full response: {tx_response}")
            print("=================================\n")

            placed_order_id = None
            if tx_response.type == "PlaceOrder":
                print(f"Number of results: {len(tx_response.results)}")
                for idx, result in enumerate(tx_response.results):
                    print(f"\n--- Result {idx + 1} ---")
                    print(f"Result type: {result.type}")

                    if result.type == "Success":
                        event = result.event
                        placed_order_id = event.order_id
                        print(f"Order ID: {event.order_id}")
                        print(f"Order IX: {event.order_ix}")
                        print(f"Account: {event.account}")
                        print(f"Instrument: {event.instrument}")

                        event_data = event.event_data
                        print(f"Event data type: {type(event_data).__name__}")

                        if hasattr(event_data, "placed"):
                            print("✓ Event: PLACED (order is on the book)")
                            print(f"  Price (scaled): {event_data.placed.price}")
                            print(f"  Size (scaled): {event_data.placed.size}")
                            print(f"  Price scale: {event_data.placed.price_scale}")
                            print(
                                f"  Quantity scale: {event_data.placed.quantity_scale}"
                            )
                            print(
                                f"  Settlement asset: {event_data.placed.settlement_asset}"
                            )
                            print(f"  Is passive: {event_data.placed.is_passive}")
                            print(f"  Is filled: {event_data.placed.is_filled}")
                            print(
                                f"  Order quantity: {event_data.placed.order_quantity}"
                            )
                        elif hasattr(event_data, "fill"):
                            print("✓ Event: FILL (order was immediately filled!)")
                            print(f"  Price (scaled): {event_data.fill.price}")
                            print(f"  Size (scaled): {event_data.fill.size}")
                            print(f"  Price scale: {event_data.fill.price_scale}")
                            print(f"  Quantity scale: {event_data.fill.quantity_scale}")
                            print(
                                f"  Settlement asset: {event_data.fill.settlement_asset}"
                            )
                            print(f"  PnL: {event_data.fill.pnl}")
                            print(f"  Is passive: {event_data.fill.is_passive}")
                            print(f"  Is filled: {event_data.fill.is_filled}")
                            print(f"  Order quantity: {event_data.fill.order_quantity}")
                            print(f"  Fee rate: {event_data.fill.fee_rate}")
                            print(f"  Fee amount: {event_data.fill.fee_amount}")
                        elif hasattr(event_data, "canceled"):
                            print("✓ Event: CANCELED")
                        elif hasattr(event_data, "modified"):
                            print("✓ Event: MODIFIED")
                            print(f"  Price (scaled): {event_data.modified.price}")
                            print(f"  Size (scaled): {event_data.modified.size}")
                        elif hasattr(event_data, "rejected"):
                            print("✗ Event: REJECTED")
                            print(f"  Reason: {event_data.rejected.reason}")
                    elif result.type == "Err":
                        print(f"✗ Order failed: {result.message}")
            elif tx_response.type == "Err":
                print(f"✗ Transaction failed: {tx_response.message}")
            print()

        except Exception as e:
            print(f"Error placing order: {e}")
            import traceback

            traceback.print_exc()
            print()

        print("Waiting 3 seconds for order book to update...")
        time.sleep(3)

        print("Fetching collateral after order placement...")
        collateral_after = sdk.get_collateral()
        collaterals_after = collateral_after.collaterals.root
        print("Collateral after order:")
        for asset_id, balance in collaterals_after.items():
            print(f"  Asset ID {asset_id}: {balance}")
        print()

        print("Fetching open orders after placement...")
        orders_response = sdk.get_open_orders()
        print(f"Open orders: {len(orders_response.orders)}")
        if orders_response.orders:
            for order in orders_response.orders:
                print(
                    f"  Order {order.order_id}: {order.side} {order.quantity} @ {order.price}"
                )
                if order.order_id == placed_order_id:
                    print("    ✓ This is the order we just placed!")
        else:
            print("  (No open orders)")
        print()

        if placed_order_id:
            if orders_response.orders and any(
                o.order_id == placed_order_id for o in orders_response.orders
            ):
                print(f"✓ Order {placed_order_id} is successfully on the order book!")
            else:
                print(f"✗ Order {placed_order_id} is NOT in open orders.")
                print()
                print("Possible reasons:")
                print(
                    "  1. Order was immediately filled (but event said is_filled=False)"
                )
                print(
                    "  2. Order was rejected after placement due to margin requirements"
                )
                print("  3. Stream state hasn't updated yet (try waiting longer)")
                print("  4. Order storage issue on the server")
                print()
                print("Debug info:")
                print(
                    f"  - Settlement asset: {instrument.settlement_asset} (should be 0 for USDC)"
                )
                print(f"  - Your USDC balance: {collaterals.get(0, '0')}")
                quantity_float = float(quantity) / instrument.quantity_scale
                order_value = bid_price * quantity_float
                print(
                    f"  - Order value: {bid_price} * {quantity_float} = {order_value}"
                )
        print()

        if orders_response.orders:
            order_to_cancel = orders_response.orders[0]
            print(f"Canceling order {order_to_cancel.order_id}...")
            try:
                cancel_response = sdk.cancel_order(order_to_cancel.order_id)
                print(f"Cancel response type: {cancel_response.type}")
                print()
            except Exception as e:
                print(f"Error canceling order: {e}")
                print()

        print("Example completed successfully!")


if __name__ == "__main__":
    main()

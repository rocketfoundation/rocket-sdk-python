from rocket_sdk_python.client.rest import RestClient
from rocket_sdk_python.crypto.signer import AccountSigner
from rocket_sdk_python.tx.builder import (
    create_vault as build_create_vault,
    place_order as build_place_order,
    set_leverage as build_set_leverage,
    vault_deposit as build_vault_deposit,
    vault_withdraw as build_vault_withdraw,
    withdraw as build_withdraw,
)
from rocket_sdk_python.tx.sign import sign_transaction
from rocket_sdk_python.types.primitives import (
    AccountAddress,
    AssetId,
    GlobalOrderId,
    InstrumentId,
    OrderSide,
)
from rocket_sdk_python.types.rest import (
    GetCollateralsResponse,
    GetOpenOrdersResponse,
    GetPositionsResponse,
)
from rocket_sdk_python.types.transaction.instruction import (
    CancelAllOrder,
    CancelAllOrderRequest,
    CancelOrder,
    CancelOrderRequest,
    LimitOrder,
    MarketOrder,
    ModifyOrder,
    ModifyOrderRequest,
    PlaceLimitOrderRequest,
    PlaceMarketOrderRequest,
)
from rocket_sdk_python.types.transaction.response import TransactionResponse


class RocketSDK:
    def __init__(self, private_key: str, rpc_url: str):
        self._signer = AccountSigner.from_private_key(private_key)
        self._client = RestClient(rpc_url)

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    @property
    def address(self) -> AccountAddress:
        return self._signer.address

    def _next_nonce(self) -> int:
        return self._client.get_account_nonce(self._signer.address)

    def place_limit_order(
        self,
        instrument_id: InstrumentId,
        side: OrderSide,
        price: str,
        quantity: str,
        reduce_only: bool = False,
        take_profit: bool = False,
        trigger_price: str | None = None,
    ) -> TransactionResponse:
        order = LimitOrder(
            Limit=PlaceLimitOrderRequest(
                instrument_id=instrument_id,
                side=side,
                price=price,
                quantity=quantity,
                trader=self._signer.address,
                reduce_only=reduce_only,
                take_profit=take_profit,
                trigger_price=trigger_price,
            )
        )
        raw_tx = build_place_order(self._signer.address, [order], self._next_nonce())
        tx = sign_transaction(raw_tx, self._signer)
        return self._client.submit_transaction(tx)

    def place_market_order(
        self,
        instrument_id: InstrumentId,
        side: OrderSide,
        quantity: str,
        reduce_only: bool = False,
        take_profit: bool = False,
        trigger_price: str | None = None,
        max_slippage: str | None = None,
    ) -> TransactionResponse:
        order = MarketOrder(
            Market=PlaceMarketOrderRequest(
                instrument_id=instrument_id,
                side=side,
                quantity=quantity,
                trader=self._signer.address,
                reduce_only=reduce_only,
                take_profit=take_profit,
                trigger_price=trigger_price,
                max_slippage=max_slippage,
            )
        )
        raw_tx = build_place_order(self._signer.address, [order], self._next_nonce())
        tx = sign_transaction(raw_tx, self._signer)
        return self._client.submit_transaction(tx)

    def cancel_order(self, order_id: GlobalOrderId) -> TransactionResponse:
        order = CancelOrder(
            Cancel=CancelOrderRequest(
                order_id=order_id,
                trader=self._signer.address,
            )
        )
        raw_tx = build_place_order(self._signer.address, [order], self._next_nonce())
        tx = sign_transaction(raw_tx, self._signer)
        return self._client.submit_transaction(tx)

    def cancel_all_orders(
        self, instrument_id: InstrumentId | None = None
    ) -> TransactionResponse:
        order = CancelAllOrder(
            CancelAll=CancelAllOrderRequest(
                instrument_id=instrument_id,
                trader=self._signer.address,
            )
        )
        raw_tx = build_place_order(self._signer.address, [order], self._next_nonce())
        tx = sign_transaction(raw_tx, self._signer)
        return self._client.submit_transaction(tx)

    def set_leverage(
        self,
        instrument_id: InstrumentId,
        leverage: int,
        account: AccountAddress | None = None,
    ) -> TransactionResponse:
        to = account if account is not None else self._signer.address
        raw_tx = build_set_leverage(
            self._signer.address, to, instrument_id, leverage, self._next_nonce()
        )
        tx = sign_transaction(raw_tx, self._signer)
        return self._client.submit_transaction(tx)

    def modify_order(
        self,
        order_id: GlobalOrderId,
        new_price: str,
        new_quantity: str,
        new_trigger_price: str | None = None,
    ) -> TransactionResponse:
        order = ModifyOrder(
            Modify=ModifyOrderRequest(
                order_id=order_id,
                new_price=new_price,
                new_quantity=new_quantity,
                trader=self._signer.address,
                new_trigger_price=new_trigger_price,
            )
        )
        raw_tx = build_place_order(self._signer.address, [order], self._next_nonce())
        tx = sign_transaction(raw_tx, self._signer)
        return self._client.submit_transaction(tx)

    def withdraw(
        self,
        asset_id: AssetId,
        amount: str,
        to: AccountAddress,
    ) -> TransactionResponse:
        raw_tx = build_withdraw(
            sender=self._signer.address,
            asset_id=asset_id,
            amount=amount,
            to=to,
            nonce=self._next_nonce(),
        )
        tx = sign_transaction(raw_tx, self._signer)
        return self._client.submit_transaction(tx)

    def get_positions(
        self, instrument_id: InstrumentId | None = None
    ) -> GetPositionsResponse:
        return self._client.get_positions(self._signer.address, instrument_id)

    def get_collateral(self, asset_id: AssetId | None = None) -> GetCollateralsResponse:
        return self._client.get_collateral(self._signer.address, asset_id)

    def get_open_orders(
        self, page_number: int | None = None, page_size: int | None = None
    ) -> GetOpenOrdersResponse:
        return self._client.get_open_orders(
            self._signer.address, page_number, page_size
        )

    def create_vault(
        self,
        deposit_asset: AssetId,
        initial_deposit: str,
    ) -> TransactionResponse:
        raw_tx = build_create_vault(
            sender=self._signer.address,
            deposit_asset=deposit_asset,
            initial_deposit=initial_deposit,
            nonce=self._next_nonce(),
        )
        tx = sign_transaction(raw_tx, self._signer)
        return self._client.submit_transaction(tx)

    def vault_deposit(
        self,
        vault: AccountAddress,
        amount: str,
    ) -> TransactionResponse:
        raw_tx = build_vault_deposit(
            sender=self._signer.address,
            vault=vault,
            amount=amount,
            nonce=self._next_nonce(),
        )
        tx = sign_transaction(raw_tx, self._signer)
        return self._client.submit_transaction(tx)

    def vault_withdraw(
        self,
        vault: AccountAddress,
        shares: str,
    ) -> TransactionResponse:
        raw_tx = build_vault_withdraw(
            sender=self._signer.address,
            vault=vault,
            shares=shares,
            nonce=self._next_nonce(),
        )
        tx = sign_transaction(raw_tx, self._signer)
        return self._client.submit_transaction(tx)

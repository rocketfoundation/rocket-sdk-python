from enum import Enum
from typing import Annotated, Union

from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.base import AccountAddress, GlobalOrderId, InstrumentId


class OrderSide(str, Enum):
    BUY = "Buy"
    SELL = "Sell"


class PlaceLimitOrderRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: InstrumentId = Field(alias="instrumentId")
    side: OrderSide
    price: str
    quantity: str
    trader: AccountAddress
    trigger_price: str | None = Field(default=None, alias="triggerPrice")
    reduce_only: bool = Field(alias="reduceOnly")
    take_profit: bool = Field(alias="takeProfit")


class PlaceMarketOrderRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: InstrumentId = Field(alias="instrumentId")
    side: OrderSide
    quantity: str
    trader: AccountAddress
    trigger_price: str | None = Field(default=None, alias="triggerPrice")
    reduce_only: bool = Field(alias="reduceOnly")
    take_profit: bool = Field(alias="takeProfit")
    max_slippage: str | None = Field(default=None, alias="maxSlippage")


class CancelOrderRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    order_id: GlobalOrderId = Field(alias="orderId")
    trader: AccountAddress


class CancelAllOrderRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: InstrumentId | None = Field(default=None, alias="instrumentId")
    trader: AccountAddress


class ModifyOrderRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    order_id: GlobalOrderId = Field(alias="orderId")
    new_price: str = Field(alias="newPrice")
    trader: AccountAddress
    new_quantity: str = Field(alias="newQuantity")
    new_trigger_price: str | None = Field(default=None, alias="newTriggerPrice")


class LimitOrder(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    Limit: PlaceLimitOrderRequest


class MarketOrder(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    Market: PlaceMarketOrderRequest


class CancelOrder(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    Cancel: CancelOrderRequest


class CancelAllOrder(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    CancelAll: CancelAllOrderRequest


class ModifyOrder(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    Modify: ModifyOrderRequest


OrderRequest = Annotated[
    Union[LimitOrder, MarketOrder, CancelOrder, CancelAllOrder, ModifyOrder],
    Field(discriminator=None),
]

OrderRequestSet = list[OrderRequest]

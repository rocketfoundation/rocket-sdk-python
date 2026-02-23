from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, RootModel

from rocket_sdk_python.types.primitives.aliases import (
    AssetId,
    BlockTimestamp,
    FeeRate,
    GlobalOrderId,
    InstrumentId,
    OrderIx,
    PriceScale,
    PriceTick,
    QuantityScale,
    QuantityTick,
)
from rocket_sdk_python.types.primitives.account_address import AccountAddress
from rocket_sdk_python.types.views.order_event import RejectionReason


class OrderEventFillFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    price: PriceTick
    size: QuantityTick
    price_scale: PriceScale = Field(alias="priceScale")
    quantity_scale: QuantityScale = Field(alias="quantityScale")
    settlement_asset: AssetId = Field(alias="settlementAsset")
    pnl: int | None = None
    timestamp: BlockTimestamp
    is_passive: bool = Field(alias="isPassive")
    is_filled: bool = Field(alias="isFilled")
    order_quantity: QuantityTick = Field(alias="orderQuantity")
    original_order_quantity: QuantityTick = Field(alias="originalOrderQuantity")
    fee_rate: FeeRate = Field(alias="feeRate")
    fee_amount: int = Field(alias="feeAmount")
    abs_position_size_change: QuantityTick = Field(alias="absPositionSizeChange")
    is_liquidation: bool = Field(alias="isLiquidation")


class OrderEventPlacedFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    price: PriceTick
    size: QuantityTick
    price_scale: PriceScale = Field(alias="priceScale")
    quantity_scale: QuantityScale = Field(alias="quantityScale")
    settlement_asset: AssetId = Field(alias="settlementAsset")
    timestamp: BlockTimestamp
    is_passive: bool = Field(alias="isPassive")
    is_filled: bool = Field(alias="isFilled")
    order_quantity: QuantityTick = Field(alias="orderQuantity")


class OrderEventModifiedFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    price: PriceTick
    size: QuantityTick
    price_scale: PriceScale = Field(alias="priceScale")
    quantity_scale: QuantityScale = Field(alias="quantityScale")
    timestamp: BlockTimestamp


class OrderEventRejectedFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    reason: RejectionReason


class OrderEventFillData(BaseModel):
    fill: OrderEventFillFields


class OrderEventPlacedData(BaseModel):
    placed: OrderEventPlacedFields


class OrderEventCanceledData(RootModel):
    root: Literal["canceled"]


class OrderEventModifiedData(BaseModel):
    modified: OrderEventModifiedFields


class OrderEventRejectedData(BaseModel):
    rejected: OrderEventRejectedFields


OrderEventData = (
    OrderEventFillData
    | OrderEventPlacedData
    | OrderEventCanceledData
    | OrderEventModifiedData
    | OrderEventRejectedData
)


class OrderEvent(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    order_id: GlobalOrderId = Field(alias="orderId")
    order_ix: OrderIx = Field(alias="orderIx")
    account: AccountAddress
    instrument: InstrumentId
    event_data: OrderEventData = Field(alias="eventData")


class PlaceOrderSuccess(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["Success"] = "Success"
    event: OrderEvent


class PlaceOrderErr(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["Err"] = "Err"
    message: str


PlaceOrderResult = Annotated[
    PlaceOrderSuccess | PlaceOrderErr,
    Field(discriminator="type"),
]

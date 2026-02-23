from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import (
    AccountAddress,
    BlockTimestamp,
    GlobalOrderId,
    InstrumentId,
    OrderSide,
)


class OrderType(str, Enum):
    LIMIT = "Limit"
    MARKET = "Market"


class TriggerType(str, Enum):
    STOP_LOSS = "StopLoss"
    TAKE_PROFIT = "TakeProfit"


class OpenOrderView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    order_id: GlobalOrderId = Field(alias="orderId")
    trader: AccountAddress
    order_type: OrderType = Field(alias="orderType")
    trigger_type: TriggerType | None = Field(default=None, alias="triggerType")
    instrument_id: InstrumentId = Field(alias="instrumentId")
    price: str
    quantity: str
    filled_quantity: str = Field(alias="filledQuantity")
    side: OrderSide
    timestamp: BlockTimestamp
    trigger_price: str | None = Field(default=None, alias="triggerPrice")

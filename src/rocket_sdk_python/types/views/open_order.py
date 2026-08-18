from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import (
    AccountAddress,
    BlockTimestamp,
    GlobalOrderId,
    InstrumentId,
    OrderSide,
)
from rocket_sdk_python.types.views.instrument_type import AggregatedInstrumentType


class OrderType(str, Enum):
    LIMIT = "Limit"
    MARKET = "Market"
    TWAP = "Twap"


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
    instrument_type: AggregatedInstrumentType = Field(
        default=AggregatedInstrumentType.UNKNOWN, alias="instrumentType"
    )
    ticker: str = ""
    underlying_asset: str = Field(default="", alias="underlyingAsset")
    price: str
    quantity: str
    filled_quantity: str = Field(alias="filledQuantity")
    side: OrderSide
    timestamp: BlockTimestamp
    trigger_price: str | None = Field(default=None, alias="triggerPrice")
    twap_interval: int | None = Field(default=None, alias="twapInterval")
    twap_original_quantity: str | None = Field(
        default=None, alias="twapOriginalQuantity"
    )
    twap_filled_quantity: str | None = Field(default=None, alias="twapFilledQuantity")
    twap_frequency: int | None = Field(default=None, alias="twapFrequency")
    twap_randomize: bool | None = Field(default=None, alias="twapRandomize")

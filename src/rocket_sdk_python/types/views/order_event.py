from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, RootModel

from rocket_sdk_python.types.primitives import (
    AccountAddress,
    AssetId,
    BlockTimestamp,
    GlobalOrderId,
    InstrumentId,
)


class RejectionReason(str, Enum):
    MARGIN_VIOLATED = "marginViolated"
    NOT_ENOUGH_LIQUIDITY = "notEnoughLiquidity"
    TOO_MUCH_SLIPPAGE = "tooMuchSlippage"
    SELF_TRADE_PREVENTION = "selfTradePrevention"
    MARKET_MAKER_PROTECTION = "marketMakerProtection"


class OrderEventFillFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    price: str
    size: str
    remaining_size: str
    original_size: str
    settlement_asset: AssetId
    pnl: str | None = None
    timestamp: BlockTimestamp
    is_passive: bool
    is_filled: bool
    fee_rate: str
    fee_amount: str
    is_liquidation: bool
    is_adl: bool = False


class OrderEventPlacedFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    price: str
    size: str
    remaining_size: str
    original_size: str
    settlement_asset: AssetId
    timestamp: BlockTimestamp
    is_passive: bool
    is_filled: bool


class OrderEventModifiedFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    price: str
    size: str
    timestamp: BlockTimestamp


class OrderEventRejectedFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    reason: RejectionReason


class OrderEventFill(BaseModel):
    fill: OrderEventFillFields


class OrderEventPlaced(BaseModel):
    placed: OrderEventPlacedFields


class OrderEventCanceled(RootModel[Literal["canceled"]]):
    root: Literal["canceled"] = "canceled"


class OrderEventModified(BaseModel):
    modified: OrderEventModifiedFields


class OrderEventRejected(BaseModel):
    rejected: OrderEventRejectedFields


OrderEventDataClientView = (
    OrderEventFill
    | OrderEventPlaced
    | OrderEventCanceled
    | OrderEventModified
    | OrderEventRejected
)


class OrderEventClientView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    order_id: GlobalOrderId = Field(alias="orderId")
    account: AccountAddress
    instrument: InstrumentId
    event_data: OrderEventDataClientView = Field(alias="eventData")

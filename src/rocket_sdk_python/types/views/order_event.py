from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

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


class OrderEventFill(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["Fill"] = "Fill"
    price: str
    size: str
    remaining_size: str = Field(alias="remainingSize")
    original_size: str = Field(alias="originalSize")
    settlement_asset: AssetId = Field(alias="settlementAsset")
    pnl: str | None = None
    timestamp: BlockTimestamp
    is_passive: bool = Field(alias="isPassive")
    is_filled: bool = Field(alias="isFilled")
    fee_rate: str = Field(alias="feeRate")
    fee_amount: str = Field(alias="feeAmount")
    is_liquidation: bool = Field(alias="isLiquidation")


class OrderEventPlaced(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["Placed"] = "Placed"
    price: str
    size: str
    remaining_size: str = Field(alias="remainingSize")
    original_size: str = Field(alias="originalSize")
    settlement_asset: AssetId = Field(alias="settlementAsset")
    timestamp: BlockTimestamp
    is_passive: bool = Field(alias="isPassive")
    is_filled: bool = Field(alias="isFilled")


class OrderEventCanceled(BaseModel):
    type: Literal["Canceled"] = "Canceled"


class OrderEventModified(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["Modified"] = "Modified"
    price: str
    size: str
    timestamp: BlockTimestamp


class OrderEventRejected(BaseModel):
    type: Literal["Rejected"] = "Rejected"
    reason: RejectionReason


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


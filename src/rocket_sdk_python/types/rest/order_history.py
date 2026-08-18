from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import (
    AccountAddress,
    AssetId,
    BlockTimestamp,
    GlobalOrderId,
    InstrumentId,
)


class GetOrderHistory(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress
    start_time: BlockTimestamp | None = Field(default=None, alias="startTime")
    end_time: BlockTimestamp | None = Field(default=None, alias="endTime")
    limit: int | None = None


class OrderHistoryResponseItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    timestamp: BlockTimestamp
    round: int
    tx_index: int = Field(alias="txIndex")
    event_index: int = Field(alias="eventIndex")
    account: AccountAddress
    instrument: InstrumentId
    order_id: GlobalOrderId = Field(alias="orderId")
    event_type: str = Field(alias="eventType")
    price: str
    size: str
    settlement_asset: AssetId = Field(alias="settlementAsset")
    pnl: str
    fee_amount: str = Field(alias="feeAmount")
    fee_rate: str = Field(alias="feeRate")
    is_passive: bool = Field(alias="isPassive")
    is_liquidation: bool = Field(alias="isLiquidation")
    is_adl: bool = Field(alias="isAdl")


class GetOrderHistoryResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    order_history: list[OrderHistoryResponseItem] = Field(alias="orderHistory")

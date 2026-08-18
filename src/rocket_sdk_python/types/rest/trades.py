from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import (
    AccountAddress,
    AssetId,
    BlockTimestamp,
    GlobalOrderId,
    InstrumentId,
)


class GetTrades(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress | None = None
    instrument: InstrumentId | None = None
    start_time: BlockTimestamp | None = Field(default=None, alias="startTime")
    end_time: BlockTimestamp | None = Field(default=None, alias="endTime")
    limit: int | None = None
    count: int | None = None
    cursor: str | None = None


class TradeResponseItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    timestamp: BlockTimestamp
    round: int
    tx_index: int = Field(alias="txIndex")
    event_index: int = Field(alias="eventIndex")
    account: AccountAddress
    instrument: InstrumentId
    ticker: str = ""
    order_id: GlobalOrderId = Field(alias="orderId")
    price: str
    size: str
    settlement_asset: AssetId = Field(alias="settlementAsset")
    pnl: str
    fee_amount: str = Field(alias="feeAmount")
    fee_rate: str = Field(alias="feeRate")
    is_passive: bool = Field(alias="isPassive")
    is_liquidation: bool = Field(alias="isLiquidation")
    is_adl: bool = Field(alias="isAdl")


class GetTradesResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    trades: list[TradeResponseItem]
    count: int | None = None
    next_cursor: str | None = Field(default=None, alias="nextCursor")

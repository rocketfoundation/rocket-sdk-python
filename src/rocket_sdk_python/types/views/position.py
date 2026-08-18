from pydantic import BaseModel, ConfigDict, Field, RootModel

from rocket_sdk_python.types.primitives import BlockTimestamp, InstrumentId
from rocket_sdk_python.types.views.instrument_type import AggregatedInstrumentType


class PositionView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    quantity: str
    average_price: str = Field(alias="averagePrice")
    liquidation_price: str = Field(alias="liquidationPrice")
    accrued_funding: str = Field(alias="accruedFunding")
    unrealized_pnl: str = Field(alias="unrealizedPnl")
    reserved_margin: str = Field(alias="reservedMargin")
    allocated_initial_margin: str = Field(default="", alias="allocatedInitialMargin")
    standalone_initial_margin: str = Field(default="", alias="standaloneInitialMargin")
    leverage_setting: int | None = Field(default=None, alias="leverageSetting")
    created_at: BlockTimestamp = Field(default=0, alias="createdAt")
    updated_at: BlockTimestamp = Field(default=0, alias="updatedAt")
    instrument_type: AggregatedInstrumentType = Field(
        default=AggregatedInstrumentType.UNKNOWN, alias="instrumentType"
    )
    ticker: str = ""
    underlying_ticker: str = Field(default="", alias="underlyingTicker")


PositionSetView = RootModel[dict[InstrumentId, PositionView]]

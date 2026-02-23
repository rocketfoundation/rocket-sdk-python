from pydantic import BaseModel, ConfigDict, Field, RootModel

from rocket_sdk_python.types.primitives import (
    AccountAddress,
    BlockTimestamp,
    InstrumentId,
)


class PositionFundingEventView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    funding_rate: str = Field(alias="fundingRate")
    timestamp: BlockTimestamp
    round: int
    instrument_id: InstrumentId = Field(alias="instrumentId")
    pnl: str
    account: AccountAddress
    position_quantity: str = Field(alias="positionQuantity")
    instrument_mark_price: str = Field(alias="instrumentMarkPrice")


PositionFundingEventsClientViewSet = RootModel[list[PositionFundingEventView]]

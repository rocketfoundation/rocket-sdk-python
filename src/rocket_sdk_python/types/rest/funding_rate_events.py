from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import InstrumentId, Round
from rocket_sdk_python.types.views import FundingRateView


class GetFundingRateEvents(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: InstrumentId = Field(alias="instrumentId")
    start_round: Round | None = Field(default=None, alias="startRound")
    end_round: Round | None = Field(default=None, alias="endRound")
    page_number: int | None = Field(default=None, alias="pageNumber")
    page_size: int | None = Field(default=None, alias="pageSize")


class GetFundingRateEventsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    events: list[FundingRateView]
    page_number: int | None = Field(default=None, alias="pageNumber")
    page_size: int | None = Field(default=None, alias="pageSize")

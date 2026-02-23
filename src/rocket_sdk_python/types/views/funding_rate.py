from pydantic import BaseModel, ConfigDict, Field, RootModel

from rocket_sdk_python.types.primitives import BlockTimestamp, InstrumentId


class FundingRateView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    funding_rate: str = Field(alias="fundingRate")
    premium_index: str = Field(alias="premiumIndex")
    timestamp: BlockTimestamp
    round: int


FundingRateByInstrumentClientView = RootModel[dict[InstrumentId, FundingRateView]]

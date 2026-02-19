from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import InstrumentId


class InstrumentStatsView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    funding_rate_1h: float = Field(alias="fundingRate1H")
    volume_24h: float = Field(alias="volume24H")
    open_interest: float = Field(alias="openInterest")


InstrumentStatsMapView = dict[InstrumentId, InstrumentStatsView]


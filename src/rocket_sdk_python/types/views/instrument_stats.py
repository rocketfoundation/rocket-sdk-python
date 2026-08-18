from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import InstrumentId


class InstrumentStatsView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    open_interest: float = Field(alias="openInterest")
    forecast_funding_rate: str | None = Field(default=None, alias="forecastFundingRate")
    premium_index: str | None = Field(default=None, alias="premiumIndex")
    volume_24h: str = Field(alias="volume24h")
    quote_volume_24h: str = Field(alias="quoteVolume24h")
    price_change_24h: str = Field(alias="priceChange24h")


InstrumentStatsMapView = dict[InstrumentId, InstrumentStatsView]

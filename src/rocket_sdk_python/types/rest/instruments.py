from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import BlockTimestamp
from rocket_sdk_python.types.views import (
    InstrumentStatsMapView,
    InstrumentsSetView,
)


class GetInstruments(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    page_number: int | None = Field(default=None, alias="pageNumber")
    page_size: int | None = Field(default=None, alias="pageSize")
    contract_type: str | None = Field(default=None, alias="contractType")
    expiry: str | None = None
    underlying_asset: str | None = Field(default=None, alias="underlyingAsset")


class InstrumentDailyPriceChange(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    price_change_quote: str = Field(alias="priceChangeQuote")
    actual_available_data_time_range_ms: BlockTimestamp = Field(
        alias="actualAvailableDataTimeRangeMs"
    )


class GetInstrumentsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instruments: InstrumentsSetView
    instrument_stats: InstrumentStatsMapView = Field(
        default_factory=dict, alias="instrumentStats"
    )

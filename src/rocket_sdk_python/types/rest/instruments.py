from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import BlockTimestamp, InstrumentId
from rocket_sdk_python.types.rest.pagination import PaginationData
from rocket_sdk_python.types.views import (
    FundingRateByInstrumentClientView,
    InstrumentStatsMapView,
    InstrumentsSetView,
)

GetInstruments = PaginationData


class InstrumentDailyPriceChange(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    price_change_quote: str = Field(alias="priceChangeQuote")
    actual_available_data_time_range_ms: BlockTimestamp = Field(
        alias="actualAvailableDataTimeRangeMs"
    )


class GetInstrumentsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instruments: InstrumentsSetView
    instrument_stats: InstrumentStatsMapView = Field(alias="instrumentStats")
    funding_rates: FundingRateByInstrumentClientView = Field(alias="fundingRates")
    daily_changes: dict[InstrumentId, InstrumentDailyPriceChange] = Field(
        alias="dailyChanges"
    )

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import BlockTimestamp, InstrumentId


class CandleTimeframe(str, Enum):
    M1 = "1m"
    M5 = "5m"
    M15 = "15m"
    M30 = "30m"
    H1 = "1h"
    H4 = "4h"
    D1 = "1d"


class GetCandles(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: InstrumentId = Field(alias="instrumentId")
    interval: CandleTimeframe
    start_time: BlockTimestamp | None = Field(default=None, alias="startTime")
    end_time: BlockTimestamp | None = Field(default=None, alias="endTime")
    limit: int | None = None


class CandleResponseItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    slot: int
    timestamp: BlockTimestamp
    open: float
    high: float
    low: float
    close: float
    volume: float


class GetCandlesResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    candles: list[CandleResponseItem]


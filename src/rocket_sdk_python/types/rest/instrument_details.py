from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import InstrumentId


class GetInstrumentDetails(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: InstrumentId | None = Field(default=None, alias="instrumentId")
    contract_type: str | None = Field(default=None, alias="contractType")
    expiry: str | None = None
    underlying_asset: str | None = Field(default=None, alias="underlyingAsset")


class InstrumentDetailsResponseItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: InstrumentId = Field(alias="instrumentId")
    volume24hr: str
    quote_volume: str = Field(alias="quoteVolume")
    trade_count: int = Field(alias="tradeCount")
    change24hr: str


class GetInstrumentDetailsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instruments: list[InstrumentDetailsResponseItem]

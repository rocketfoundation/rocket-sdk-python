from pydantic import BaseModel, ConfigDict, Field, RootModel

from rocket_sdk_python.types.primitives import InstrumentId


class InstrumentView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    ticker: str
    instrument_type: str = Field(alias="instrumentType")
    underlying_asset: str = Field(alias="underlyingAsset")
    settlement_asset: str = Field(alias="settlementAsset")
    is_trading: bool = Field(alias="isTrading")
    expiry: str | None = None
    strike: str | None = None
    price_scale: int = Field(alias="priceScale")
    quantity_scale: int = Field(alias="quantityScale")
    worst_case_price_move_pct: str | None = Field(default=None, alias="worstCasePriceMovePct")
    max_leverage: str | None = Field(default=None, alias="maxLeverage")
    last_match_price: str = Field(alias="lastMatchPrice")
    worst_case_price_move_pct_margin: str | None = Field(default=None, alias="worstCasePriceMovePctMargin")
    max_leverage_margin: str | None = Field(default=None, alias="maxLeverageMargin")


InstrumentsSetView = RootModel[dict[InstrumentId, InstrumentView]]


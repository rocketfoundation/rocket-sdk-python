from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives.aliases import AssetTicker


class SourceId(str, Enum):
    MOCK = "Mock"
    DERIBIT = "Deribit"
    BINANCE_SPOT = "BinanceSpot"
    MEXC = "MEXC"
    PYTH = "Pyth"
    HYPERLIQUID = "Hyperliquid"
    COMMODITIES_API = "CommoditiesAPI"


class OraclePriceScale(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    numerator: int
    denominator: int


class OracleState(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    asset_ticker_overrides: dict[AssetTicker, AssetTicker] = Field(
        default_factory=dict, alias="assetTickerOverrides"
    )
    price_scales: dict[AssetTicker, OraclePriceScale] = Field(
        default_factory=dict, alias="priceScales"
    )


OracleSettingsMap = dict[SourceId, OracleState]


from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives.aliases import (
    AssetId,
    BlockTimestamp,
    InstrumentFlags,
    InstrumentId,
    PnLTick,
    PriceScale,
    PriceTick,
    QuantityScale,
    QuantityTick,
)

SPOT_INSTRUMENT: InstrumentFlags = 1 << 0
PERPETUAL_INSTRUMENT: InstrumentFlags = 1 << 1
FUTURE_INSTRUMENT: InstrumentFlags = 1 << 2
CALL_OPTION_INSTRUMENT: InstrumentFlags = 1 << 3
PUT_OPTION_INSTRUMENT: InstrumentFlags = 1 << 4

PnLGrid = list[PnLTick]


class InstrumentRow(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: InstrumentId = Field(alias="instrumentId")
    underlying_asset_id: AssetId = Field(alias="underlyingAssetId")
    settlement_asset_id: AssetId = Field(alias="settlementAssetId")
    expiry: BlockTimestamp
    strike: PriceTick
    price_scale: PriceScale = Field(alias="priceScale")
    quantity_scale: QuantityScale = Field(alias="quantityScale")
    instrument_flags: InstrumentFlags = Field(alias="instrumentFlags")
    mark_price: PriceTick = Field(alias="markPrice")
    is_trading: bool = Field(alias="isTrading")
    last_match_price: PriceTick = Field(alias="lastMatchPrice")
    last_match_volume: QuantityTick = Field(alias="lastMatchVolume")
    pnl_grid: PnLGrid = Field(alias="pnlGrid")
    initial_pnl_grid: PnLGrid = Field(alias="initialPnlGrid")


class InstrumentRowData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    underlying_asset_id: AssetId = Field(alias="underlyingAssetId")
    settlement_asset_id: AssetId = Field(alias="settlementAssetId")
    expiry: BlockTimestamp
    strike: PriceTick
    price_scale: PriceScale = Field(alias="priceScale")
    quantity_scale: QuantityScale = Field(alias="quantityScale")
    instrument_flags: InstrumentFlags = Field(alias="instrumentFlags")
    is_trading: bool = Field(alias="isTrading")
    pnl_grid: PnLGrid = Field(alias="pnlGrid")
    initial_pnl_grid: PnLGrid = Field(alias="initialPnlGrid")


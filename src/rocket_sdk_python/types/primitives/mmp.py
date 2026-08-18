from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives.aliases import AssetId, BlockTimestamp, MMPTag

DEFAULT_MMP_TAG: MMPTag = 0


class MarketMakerProtectionConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    mmp_underlying_asset_id: AssetId = Field(alias="mmpUnderlyingAssetId")
    quantity_limit: int | None = Field(
        default=None,
        validation_alias=AliasChoices("quantityLimit", "notionalQuantityLimit"),
        serialization_alias="quantityLimit",
    )
    delta_limit: int | None = Field(default=None, alias="deltaLimit")
    window: BlockTimestamp
    freeze: BlockTimestamp
    mmp_max_quote_quantity: int = Field(alias="mmpMaxQuoteQuantity")

from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import (
    AccountAddress,
    MMPTag,
    MarketMakerProtectionConfig,
)


class SetMarketMakerProtectionData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    to: AccountAddress
    mmp_tag: MMPTag = Field(alias="mmpTag")
    config: MarketMakerProtectionConfig


class SetMarketMakerProtectionInstruction(BaseModel):
    SetMarketMakerProtection: SetMarketMakerProtectionData

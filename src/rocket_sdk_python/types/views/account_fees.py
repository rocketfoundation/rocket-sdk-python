from pydantic import BaseModel, ConfigDict, Field

LiquidityProviderRank = int


class AccountFeesClientView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    passive: str
    active: str
    total_volume: str = Field(alias="totalVolume")
    liquidity_provider_rank: LiquidityProviderRank = Field(alias="liquidityProviderRank")
    tier: str


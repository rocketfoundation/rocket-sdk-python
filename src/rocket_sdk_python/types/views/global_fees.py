from pydantic import BaseModel, ConfigDict, Field, RootModel


class FeeRatesClientView(BaseModel):
    passive: str
    active: str


FeeLadderClientView = RootModel[list[tuple[str, FeeRatesClientView]]]

LiquidityProviderTierLevel = int

LiquidityProviderFeeRankingClientView = RootModel[
    list[tuple[LiquidityProviderTierLevel, FeeRatesClientView]]
]


class GlobalFeesClientView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    regular_fee_ladder: FeeLadderClientView = Field(alias="regularFeeLadder")
    liquidity_provider_fee_ranking: LiquidityProviderFeeRankingClientView = Field(
        alias="liquidityProviderFeeRanking"
    )


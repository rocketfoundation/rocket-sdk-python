from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import AccountAddress


class GetVaultPortfolio(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress
    vault: AccountAddress | None = None


class VaultPortfolioPosition(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    vault: AccountAddress
    shares: str
    total_shares: str = Field(alias="totalShares")
    vault_equity: str = Field(alias="vaultEquity")
    value: str
    deposits: str
    withdrawals: str
    pnl: str


class GetVaultPortfolioResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    positions: list[VaultPortfolioPosition]

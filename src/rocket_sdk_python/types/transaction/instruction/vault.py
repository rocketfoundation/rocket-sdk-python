from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import AccountAddress, AssetId


class CreateVaultData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    deposit_asset: AssetId = Field(alias="depositAsset")
    initial_deposit: str = Field(alias="initialDeposit")


class VaultDepositData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    vault: AccountAddress
    amount: str


class VaultWithdrawData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    vault: AccountAddress
    shares: str


class CreateVaultInstruction(BaseModel):
    CreateVault: CreateVaultData


class VaultDepositInstruction(BaseModel):
    VaultDeposit: VaultDepositData


class VaultWithdrawInstruction(BaseModel):
    VaultWithdraw: VaultWithdrawData


from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import AccountAddress
from rocket_sdk_python.types.views.vault_depositors import VaultDepositorsView


class GetVaultDepositors(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    vault: AccountAddress


class GetVaultDepositorsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    vault_depositors: VaultDepositorsView = Field(alias="vaultDepositors")

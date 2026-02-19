from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import AccountAddress, BlockTimestamp
from rocket_sdk_python.types.views import VaultStatsSetView


class GetVaultStats(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    vault_addresses: list[AccountAddress] | None = Field(
        default=None, alias="vaultAddresses"
    )
    from_: BlockTimestamp = Field(alias="from")
    to: BlockTimestamp


class GetVaultStatsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    vault_stats: VaultStatsSetView = Field(alias="vaultStats")


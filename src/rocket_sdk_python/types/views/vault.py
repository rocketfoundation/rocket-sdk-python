from pydantic import BaseModel, ConfigDict, Field, RootModel

from rocket_sdk_python.types.primitives import AccountAddress, AssetId, BlockTimestamp


class VaultView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    address: AccountAddress
    manager: AccountAddress
    asset: AssetId
    is_main: bool = Field(default=False, alias="isMain")
    creation_timestamp: BlockTimestamp = Field(alias="creationTimestamp")


VaultSetView = RootModel[list[VaultView]]

from pydantic import BaseModel, ConfigDict, RootModel

from rocket_sdk_python.types.primitives import AccountAddress


class VaultDepositorView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress
    shares: str = "0"
    value: str = "0"


VaultDepositorsView = RootModel[list[VaultDepositorView]]

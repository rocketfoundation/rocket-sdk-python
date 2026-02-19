from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import AccountAddress
from rocket_sdk_python.types.views import VaultHistoryClientView


class GetVaultHistory(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    vault: AccountAddress
    user: AccountAddress | None = None
    page_number: int | None = Field(default=None, alias="pageNumber")
    page_size: int | None = Field(default=None, alias="pageSize")


class GetVaultHistoryResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    history: VaultHistoryClientView
    page_number: int | None = Field(default=None, alias="pageNumber")
    page_size: int | None = Field(default=None, alias="pageSize")


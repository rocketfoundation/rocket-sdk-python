from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import AccountAddress
from rocket_sdk_python.types.views import AccountFeesClientView


class GetAccountFees(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress


class GetAccountFeesResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account_fees: AccountFeesClientView = Field(alias="accountFees")


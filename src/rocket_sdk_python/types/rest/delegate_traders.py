from pydantic import BaseModel, ConfigDict

from rocket_sdk_python.types.primitives import AccountAddress
from rocket_sdk_python.types.views.delegate_traders import DelegateTraderView


class GetDelegateTraders(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress


class GetDelegateTradersResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    delegates: list[DelegateTraderView]

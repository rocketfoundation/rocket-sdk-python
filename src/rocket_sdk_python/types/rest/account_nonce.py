from pydantic import BaseModel, ConfigDict

from rocket_sdk_python.types.primitives import AccountAddress


class GetAccountNonce(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress


class GetAccountNonceResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    nonce: int

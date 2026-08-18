from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import AccountAddress


class DelegateManagerData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    manager: AccountAddress
    expiry_ms: int | None = Field(default=None, alias="expiryMs")
    name: str | None = None
    is_web_client: bool | None = Field(default=None, alias="isWebClient")


class RemoveDelegateManagerData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    manager: AccountAddress


class RemoveWebclientDelegatesData(BaseModel):
    pass


class DelegateManagerInstruction(BaseModel):
    DelegateManager: DelegateManagerData


class RemoveDelegateManagerInstruction(BaseModel):
    RemoveDelegateManager: RemoveDelegateManagerData


class RemoveWebclientDelegatesInstruction(BaseModel):
    RemoveWebclientDelegates: RemoveWebclientDelegatesData

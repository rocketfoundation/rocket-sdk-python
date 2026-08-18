from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import AccountAddress


class DelegateTraderView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    address: AccountAddress
    expiry_ms: int | None = Field(default=None, alias="expiryMs")
    name: str | None = None
    is_web_client: bool = Field(alias="isWebClient")

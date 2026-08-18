from pydantic import BaseModel, ConfigDict, Field


class GetExpirations(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    contract_type: str = Field(alias="contractType")
    underlying_asset: str = Field(alias="underlyingAsset")


class GetExpirationsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    expirations: list[str]

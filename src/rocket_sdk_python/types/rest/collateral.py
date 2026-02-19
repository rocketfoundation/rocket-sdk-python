from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import AccountAddress, AssetId
from rocket_sdk_python.types.views import CollateralView


class GetCollateral(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress
    asset_id: AssetId | None = Field(default=None, alias="assetId")


class GetCollateralsResponse(BaseModel):
    collaterals: CollateralView


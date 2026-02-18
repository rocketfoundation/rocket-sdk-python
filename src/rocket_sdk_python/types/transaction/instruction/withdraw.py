from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import AssetId


class WithdrawData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    asset_id: AssetId = Field(alias="assetId")
    amount: str
    to: str


class WithdrawInstruction(BaseModel):
    Withdraw: WithdrawData


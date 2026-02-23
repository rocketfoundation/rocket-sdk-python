from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import AccountAddress, BlockTimestamp


class GetFaucetClaim(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress


class GetFaucetClaimResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    last_claim_timestamp: BlockTimestamp | None = Field(
        default=None, alias="lastClaimTimestamp"
    )

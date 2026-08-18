from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import (
    AccountAddress,
    AssetId,
    BlockTimestamp,
    Round,
)


class GetVaultEvents(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    vault: AccountAddress | None = None
    account: AccountAddress | None = None
    round_from: str | None = Field(default=None, alias="roundFrom")
    round_to: str | None = Field(default=None, alias="roundTo")
    page_number: int | None = Field(default=None, alias="pageNumber")
    page_size: int | None = Field(default=None, alias="pageSize")


class VaultEventResponseItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    timestamp: BlockTimestamp
    round: Round
    tx_index: int = Field(alias="txIndex")
    event_index: int = Field(alias="eventIndex")
    vault: AccountAddress
    account: AccountAddress
    event_type: str = Field(alias="eventType")
    asset_id: AssetId = Field(alias="assetId")
    amount: str
    shares: str
    tx_hash: str = Field(alias="txHash")


class GetVaultEventsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    events: list[VaultEventResponseItem]
    page_number: int | None = Field(default=None, alias="pageNumber")
    page_size: int | None = Field(default=None, alias="pageSize")

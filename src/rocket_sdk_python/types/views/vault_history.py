from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, RootModel

from rocket_sdk_python.types.primitives import (
    AccountAddress,
    AssetId,
    BlockTimestamp,
    Round,
    Shares,
)


class VaultHistoryEventType(str, Enum):
    DEPOSIT = "Deposit"
    WITHDRAW = "Withdraw"


class VaultHistoryEntryClientView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    event_type: VaultHistoryEventType = Field(alias="eventType")
    vault: AccountAddress
    user: AccountAddress
    asset_id: AssetId = Field(alias="assetId")
    amount: str
    shares: Shares
    timestamp: BlockTimestamp
    round: Round
    tx_hash: str = Field(alias="txHash")


VaultHistoryClientView = RootModel[list[VaultHistoryEntryClientView]]


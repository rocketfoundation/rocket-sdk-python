from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, RootModel

from rocket_sdk_python.types.primitives import AccountAddress, BlockTimestamp


class BridgeEventType(str, Enum):
    DEPOSIT = "Deposit"
    WITHDRAW = "Withdraw"


class BridgeEventClientView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    round: int
    timestamp: BlockTimestamp
    account_address: AccountAddress = Field(alias="accountAddress")
    external_address: str = Field(alias="externalAddress")
    external_token_address: str = Field(alias="externalTokenAddress")
    id: int
    amount: str
    event_type: BridgeEventType = Field(alias="eventType")


BridgeEventsSetClientView = RootModel[list[BridgeEventClientView]]

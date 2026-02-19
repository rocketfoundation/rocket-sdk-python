from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import AccountAddress
from rocket_sdk_python.types.views import BridgeEventsSetClientView


class GetBridgeEvents(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress | None = None
    round_from: str | None = Field(default=None, alias="roundFrom")
    round_to: str | None = Field(default=None, alias="roundTo")
    page_number: int | None = Field(default=None, alias="pageNumber")
    page_size: int | None = Field(default=None, alias="pageSize")


class GetBridgeEventsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    events: BridgeEventsSetClientView


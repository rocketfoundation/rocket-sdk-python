from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import AccountAddress
from rocket_sdk_python.types.views import PositionFundingEventsClientViewSet


class GetAccountPositionFundingEvents(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress
    page_number: int | None = Field(default=None, alias="pageNumber")
    page_size: int | None = Field(default=None, alias="pageSize")


class GetPositionFundingEventsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    events: PositionFundingEventsClientViewSet | None = None
    page_number: int | None = Field(default=None, alias="pageNumber")
    page_size: int | None = Field(default=None, alias="pageSize")

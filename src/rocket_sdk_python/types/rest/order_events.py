from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import AccountAddress
from rocket_sdk_python.types.views import OrderEventClientView


class GetAccountOrderEvents(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress
    page_number: int | None = Field(default=None, alias="pageNumber")
    page_size: int | None = Field(default=None, alias="pageSize")


class GetOrderEventsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    order_events: list[OrderEventClientView] | None = Field(
        default=None, alias="orderEvents"
    )
    page_number: int | None = Field(default=None, alias="pageNumber")
    page_size: int | None = Field(default=None, alias="pageSize")

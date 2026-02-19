from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import AccountAddress
from rocket_sdk_python.types.rest.pagination import PaginationData
from rocket_sdk_python.types.views import OpenOrderView


class GetOpenOrders(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress
    page_number: int | None = Field(default=None, alias="pageNumber")
    page_size: int | None = Field(default=None, alias="pageSize")


class GetOpenOrdersResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    orders: list[OpenOrderView] | None = None
    page_number: int | None = Field(default=None, alias="pageNumber")
    page_size: int | None = Field(default=None, alias="pageSize")


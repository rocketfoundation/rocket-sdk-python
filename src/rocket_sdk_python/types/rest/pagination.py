from pydantic import BaseModel, ConfigDict, Field


class PaginationData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    page_number: int | None = Field(default=None, alias="pageNumber")
    page_size: int | None = Field(default=None, alias="pageSize")

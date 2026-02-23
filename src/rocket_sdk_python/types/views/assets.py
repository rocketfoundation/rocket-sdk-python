from pydantic import BaseModel, ConfigDict, Field, RootModel

from rocket_sdk_python.types.primitives import AssetId


class AssetView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: AssetId
    ticker: str
    haircut: str
    mark_price: str = Field(alias="markPrice")


AssetSetView = RootModel[dict[AssetId, AssetView]]

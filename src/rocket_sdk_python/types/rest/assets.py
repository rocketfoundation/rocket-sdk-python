from pydantic import BaseModel

from rocket_sdk_python.types.rest.pagination import PaginationData
from rocket_sdk_python.types.views import AssetSetView

GetAssets = PaginationData


class GetAssetsResponse(BaseModel):
    assets: AssetSetView

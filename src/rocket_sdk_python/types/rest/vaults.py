from pydantic import BaseModel

from rocket_sdk_python.types.rest.pagination import PaginationData
from rocket_sdk_python.types.views import VaultSetView

GetVaults = PaginationData


class GetVaultsResponse(BaseModel):
    vaults: VaultSetView


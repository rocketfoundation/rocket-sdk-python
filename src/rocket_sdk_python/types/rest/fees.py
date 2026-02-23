from pydantic import BaseModel

from rocket_sdk_python.types.views import GlobalFeesClientView


class GetGlobalFeesResponse(BaseModel):
    result: GlobalFeesClientView

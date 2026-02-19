from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import AccountAddress, InstrumentId
from rocket_sdk_python.types.views import PositionSetView


class GetPosition(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress
    instrument_id: InstrumentId | None = Field(default=None, alias="instrumentId")


class GetPositionsResponse(BaseModel):
    positions: PositionSetView | None = None


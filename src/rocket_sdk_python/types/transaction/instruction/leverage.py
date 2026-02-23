from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import AccountAddress, InstrumentId


class SetLeverageData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    to: AccountAddress
    instrument_id: InstrumentId = Field(alias="instrumentId")
    leverage: int


class SetLeverageInstruction(BaseModel):
    SetLeverage: SetLeverageData

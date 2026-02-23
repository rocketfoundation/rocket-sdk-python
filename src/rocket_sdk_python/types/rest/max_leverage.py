from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import AccountAddress, InstrumentId


class GetMaxLeverage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress
    instrument_id: InstrumentId = Field(alias="instrumentId")


class GetMaxLeverageResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    max_leverage_setting: int = Field(alias="maxLeverageSetting")

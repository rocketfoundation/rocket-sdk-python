from pydantic import BaseModel, ConfigDict, Field, RootModel

from rocket_sdk_python.types.primitives import InstrumentId


class PositionView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    quantity: str
    average_price: str = Field(alias="averagePrice")
    liquidation_price: str = Field(alias="liquidationPrice")
    accrued_funding: str = Field(alias="accruedFunding")
    unrealized_pnl: str = Field(alias="unrealizedPnl")
    reserved_margin: str = Field(alias="reservedMargin")
    leverage_setting: int = Field(alias="leverageSetting")


PositionSetView = RootModel[dict[InstrumentId, PositionView]]

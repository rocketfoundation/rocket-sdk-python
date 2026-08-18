from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import AccountAddress, BlockTimestamp
from rocket_sdk_python.types.rest.candles import CandleTimeframe
from rocket_sdk_python.types.views.portfolio import (
    PortfolioCurvePoint,
    PortfolioSummary,
)


class GetPortfolio(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress
    from_: BlockTimestamp = Field(alias="from")
    to: BlockTimestamp
    interval: CandleTimeframe


class GetPortfolioResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    equity: list[PortfolioCurvePoint]
    pnl: list[PortfolioCurvePoint]
    summary: PortfolioSummary

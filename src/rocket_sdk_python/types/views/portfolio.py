from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import BlockTimestamp


class PortfolioCurvePoint(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    timestamp: BlockTimestamp
    value: str


class PortfolioSummary(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    pnl: str = "0"
    total_funding: str = Field(default="0", alias="totalFunding")
    volume: str = "0"
    max_drawdown_pct: str = Field(default="0", alias="maxDrawdownPct")
    return_pct: str = Field(default="0", alias="returnPct")
    avg_daily_pnl: str = Field(default="0", alias="avgDailyPnl")
    pnl_volatility_pct: str = Field(default="0", alias="pnlVolatilityPct")
    pnl_volatility_usd: str = Field(default="0", alias="pnlVolatilityUsd")
    sharpe_ratio: str = Field(default="0", alias="sharpeRatio")
    total_trades: int = Field(default=0, alias="totalTrades")
    profit_factor: str = Field(default="0", alias="profitFactor")
    win_rate: str = Field(default="0", alias="winRate")
    wins: str = "0"
    losses: str = "0"
    average_win: str = Field(default="0", alias="averageWin")
    average_loss: str = Field(default="0", alias="averageLoss")
    long_pnl: str = Field(default="0", alias="longPnl")
    short_pnl: str = Field(default="0", alias="shortPnl")


class VaultHistoryStats(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    sharpe_ratio: str = Field(default="0", alias="sharpeRatio")
    average_returns: str = Field(default="0", alias="averageReturns")
    returns_volatility: str = Field(default="0", alias="returnsVolatility")
    max_drawdown: str = Field(default="0", alias="maxDrawdown")

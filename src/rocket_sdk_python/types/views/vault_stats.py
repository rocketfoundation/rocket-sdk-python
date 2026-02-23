from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import AccountAddress, BlockTimestamp


class VaultStatsForRangeViewItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    timestamp: BlockTimestamp
    nav: float
    tvl: float
    r: float = Field(alias="return")
    r_absolute: float = Field(alias="returnAbsolute")


class VaultStatsForRangeView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    avg_returns: float = Field(alias="avgReturns")
    returns_volatility: float = Field(alias="returnsVolatility")
    max_drawdown: float = Field(alias="maxDrawdown")
    sharpe_ratio_daily: float = Field(alias="sharpeRatioDaily")
    daily_values: list[VaultStatsForRangeViewItem] = Field(alias="dailyValues")


class VaultShareBalanceView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    shares: int
    withdrawable_balance: float = Field(alias="withdrawableBalance")


class VaultStatsView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    depositors: int
    creation_timestamp: int = Field(alias="creationTimestamp")
    current_tvl: float = Field(alias="CurrentTVL")
    apr: float = Field(alias="APR")
    apr_data_time_range: BlockTimestamp = Field(alias="APRTimeRange")
    apr_30d: float = Field(alias="APR30d")
    apr_30d_data_time_range: BlockTimestamp
    stats_for_time_range: VaultStatsForRangeView = Field(alias="statsForTimeRange")
    balances: dict[AccountAddress, VaultShareBalanceView]


class VaultStatsSetViewEntry(BaseModel):
    address: AccountAddress
    stats: VaultStatsView


VaultStatsSetView = list[VaultStatsSetViewEntry]

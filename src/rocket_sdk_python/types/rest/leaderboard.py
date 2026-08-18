from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import AccountAddress, BlockTimestamp


class LeaderboardMetric(str, Enum):
    PNL = "pnl"
    VOLUME = "volume"


class GetLeaderboard(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    start_time: BlockTimestamp | None = Field(default=None, alias="startTime")
    end_time: BlockTimestamp | None = Field(default=None, alias="endTime")
    count: int | None = None
    metric: LeaderboardMetric | None = None
    account: AccountAddress | None = None


class LeaderboardResponseItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user: AccountAddress
    pnl: str
    volume: str


class LeaderboardPositionResponseItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    position: int
    user: AccountAddress
    pnl: str
    volume: str


class GetLeaderboardResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    leaderboard: list[LeaderboardResponseItem]
    account_position: LeaderboardPositionResponseItem | None = Field(
        default=None, alias="accountPosition"
    )

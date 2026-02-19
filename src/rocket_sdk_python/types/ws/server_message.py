from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import (
    AccountAddress,
    AssetId,
    BlockTimestamp,
    InstrumentId,
    Round,
)
from rocket_sdk_python.types.rest.candles import CandleTimeframe
from rocket_sdk_python.types.views import (
    InstrumentStatsView,
    OpenOrderView,
    OrderEventClientView,
    PositionSetView,
)
from rocket_sdk_python.types.ws.subscription_kind import SubscriptionKind


class QuoteView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    timestamp: int
    bid_price: str = Field(alias="bidPrice")
    bid_size: str = Field(alias="bidSize")
    ask_price: str = Field(alias="askPrice")
    ask_size: str = Field(alias="askSize")


class LevelView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    price: str
    quantity: str


class OrderbookView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    bids: list[LevelView]
    asks: list[LevelView]


class MarkPriceView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    price: str
    iv: str | None = None
    timestamp: BlockTimestamp


class AccountRiskView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress
    available_collateral: str = Field(alias="availableCollateral")
    margin_requirement: str = Field(alias="marginRequirement")
    unreserved_margin: str = Field(alias="unreservedMargin")
    equity: str
    reserved_margin: str = Field(alias="reservedMargin")
    unrealized_pnl: str = Field(alias="unrealizedPnl")
    notional_value: str = Field(alias="notionalValue")


class CandleView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: InstrumentId = Field(alias="instrumentId")
    interval: CandleTimeframe
    slot: int
    timestamp: BlockTimestamp
    open: float
    high: float
    low: float
    close: float
    volume: float
    is_closed: bool = Field(alias="isClosed")


class QuoteUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["QuoteUpdate"] = "QuoteUpdate"
    instrument_id: InstrumentId = Field(alias="instrumentId")
    quote: QuoteView


class OrderbookUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["OrderbookUpdate"] = "OrderbookUpdate"
    instrument_id: InstrumentId = Field(alias="instrumentId")
    orderbook: OrderbookView


class MarkPriceUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["MarkPriceUpdate"] = "MarkPriceUpdate"
    instrument_id: InstrumentId = Field(alias="instrumentId")
    mark_price: MarkPriceView = Field(alias="markPrice")


class AssetMarkPriceUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["AssetMarkPriceUpdate"] = "AssetMarkPriceUpdate"
    asset_id: AssetId = Field(alias="assetId")
    mark_price: MarkPriceView = Field(alias="markPrice")


class OrderEventUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["OrderEventUpdate"] = "OrderEventUpdate"
    account: AccountAddress | None = None
    instrument_id: InstrumentId | None = Field(default=None, alias="instrumentId")
    order_events: list[OrderEventClientView] = Field(alias="orderEvents")


class CollateralUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["CollateralUpdate"] = "CollateralUpdate"
    asset_id: AssetId = Field(alias="assetId")
    account: AccountAddress
    collateral: str


class PositionUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["PositionUpdate"] = "PositionUpdate"
    account: AccountAddress
    positions: PositionSetView


class AccountRiskUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["AccountRiskUpdate"] = "AccountRiskUpdate"
    account: AccountAddress
    risk: AccountRiskView


class OpenOrdersUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["OpenOrdersUpdate"] = "OpenOrdersUpdate"
    account: AccountAddress
    orders: list[OpenOrderView]


class FundingRateUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["FundingRateUpdate"] = "FundingRateUpdate"
    instrument_id: InstrumentId = Field(alias="instrumentId")
    funding_rate: str = Field(alias="fundingRate")
    premium_index: str = Field(alias="premiumIndex")
    timestamp: BlockTimestamp
    round: Round


class InstrumentStatsUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["InstrumentStatsUpdate"] = "InstrumentStatsUpdate"
    instrument_id: InstrumentId = Field(alias="instrumentId")
    stats: InstrumentStatsView


class CandleUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["CandleUpdate"] = "CandleUpdate"
    candle: CandleView


class PositionFundingUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["PositionFundingUpdate"] = "PositionFundingUpdate"
    account: AccountAddress
    funding_rate: str = Field(alias="fundingRate")
    timestamp: BlockTimestamp
    round: Round
    instrument_id: InstrumentId = Field(alias="instrumentId")
    pnl: str


class LastMatchPriceUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["LastMatchPriceUpdate"] = "LastMatchPriceUpdate"
    instrument_id: InstrumentId = Field(alias="instrumentId")
    last_match_price: str = Field(alias="lastMatchPrice")


class SubscribeConfirmation(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["SubscribeConfirmation"] = "SubscribeConfirmation"
    subscription: SubscriptionKind


class UnsubscribeConfirmation(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["UnsubscribeConfirmation"] = "UnsubscribeConfirmation"
    subscription: SubscriptionKind


class Pong(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["Pong"] = "Pong"


class ErrorMessage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["Error"] = "Error"
    message: str


ServerMessage = Annotated[
    QuoteUpdate
    | OrderbookUpdate
    | MarkPriceUpdate
    | AssetMarkPriceUpdate
    | OrderEventUpdate
    | CollateralUpdate
    | PositionUpdate
    | AccountRiskUpdate
    | OpenOrdersUpdate
    | FundingRateUpdate
    | InstrumentStatsUpdate
    | CandleUpdate
    | PositionFundingUpdate
    | LastMatchPriceUpdate
    | SubscribeConfirmation
    | UnsubscribeConfirmation
    | Pong
    | ErrorMessage,
    Field(discriminator="type"),
]


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


class QuoteUpdateFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: InstrumentId = Field(alias="instrumentId")
    quote: QuoteView


class QuoteUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    QuoteUpdate: QuoteUpdateFields


class OrderbookUpdateFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: InstrumentId = Field(alias="instrumentId")
    orderbook: OrderbookView


class OrderbookUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    OrderbookUpdate: OrderbookUpdateFields


class MarkPriceUpdateFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: InstrumentId = Field(alias="instrumentId")
    mark_price: MarkPriceView = Field(alias="markPrice")


class MarkPriceUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    MarkPriceUpdate: MarkPriceUpdateFields


class AssetMarkPriceUpdateFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    asset_id: AssetId = Field(alias="assetId")
    mark_price: MarkPriceView = Field(alias="markPrice")


class AssetMarkPriceUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    AssetMarkPriceUpdate: AssetMarkPriceUpdateFields


class OrderEventUpdateFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress | None = None
    instrument_id: InstrumentId | None = Field(default=None, alias="instrumentId")
    order_events: list[OrderEventClientView] = Field(alias="orderEvents")


class OrderEventUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    OrderEventUpdate: OrderEventUpdateFields


class CollateralUpdateFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    asset_id: AssetId = Field(alias="assetId")
    account: AccountAddress
    collateral: str


class CollateralUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    CollateralUpdate: CollateralUpdateFields


class PositionUpdateFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress
    positions: PositionSetView


class PositionUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    PositionUpdate: PositionUpdateFields


class AccountRiskUpdateFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress
    risk: AccountRiskView


class AccountRiskUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    AccountRiskUpdate: AccountRiskUpdateFields


class OpenOrdersUpdateFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress
    orders: list[OpenOrderView]


class OpenOrdersUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    OpenOrdersUpdate: OpenOrdersUpdateFields


class FundingRateUpdateFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: InstrumentId = Field(alias="instrumentId")
    funding_rate: str = Field(alias="fundingRate")
    premium_index: str = Field(alias="premiumIndex")
    timestamp: BlockTimestamp
    round: Round


class FundingRateUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    FundingRateUpdate: FundingRateUpdateFields


class InstrumentStatsUpdateFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: InstrumentId = Field(alias="instrumentId")
    stats: InstrumentStatsView


class InstrumentStatsUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    InstrumentStatsUpdate: InstrumentStatsUpdateFields


class CandleUpdateFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    candle: CandleView


class CandleUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    CandleUpdate: CandleUpdateFields


class PositionFundingUpdateFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress
    funding_rate: str = Field(alias="fundingRate")
    timestamp: BlockTimestamp
    round: Round
    instrument_id: InstrumentId = Field(alias="instrumentId")
    pnl: str


class PositionFundingUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    PositionFundingUpdate: PositionFundingUpdateFields


class LastMatchPriceUpdateFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: InstrumentId = Field(alias="instrumentId")
    last_match_price: str = Field(alias="lastMatchPrice")


class LastMatchPriceUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    LastMatchPriceUpdate: LastMatchPriceUpdateFields


class SubscribeConfirmation(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    SubscribeConfirmation: SubscriptionKind


class UnsubscribeConfirmation(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    UnsubscribeConfirmation: SubscriptionKind


class Pong(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    Pong: None = None


class ErrorMessage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    Error: str


ServerMessage = (
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
    | ErrorMessage
)


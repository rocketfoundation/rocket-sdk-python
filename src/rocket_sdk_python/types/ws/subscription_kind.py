from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import AccountAddress, AssetId, InstrumentId
from rocket_sdk_python.types.rest.candles import CandleTimeframe


class OrderbookSubscriptionFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: InstrumentId = Field(alias="instrumentId")


class OrderbookSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    Orderbook: OrderbookSubscriptionFields


class PriceFeedSubscriptionFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: InstrumentId = Field(alias="instrumentId")


class PriceFeedSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    PriceFeed: PriceFeedSubscriptionFields


class AssetPriceFeedSubscriptionFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    asset_id: AssetId = Field(alias="assetId")


class AssetPriceFeedSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    AssetPriceFeed: AssetPriceFeedSubscriptionFields


class OrderEventsSubscriptionFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress | None = None
    instrument_id: InstrumentId | None = Field(default=None, alias="instrumentId")


class OrderEventsSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    OrderEvents: OrderEventsSubscriptionFields


class CollateralSubscriptionFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    asset_id: AssetId = Field(alias="assetId")
    account: AccountAddress


class CollateralSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    Collateral: CollateralSubscriptionFields


class PositionSubscriptionFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress


class PositionSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    Position: PositionSubscriptionFields


class AccountRiskSubscriptionFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress


class AccountRiskSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    AccountRisk: AccountRiskSubscriptionFields


class OpenOrdersSubscriptionFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress


class OpenOrdersSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    OpenOrders: OpenOrdersSubscriptionFields


class FundingRateSubscriptionFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: InstrumentId = Field(alias="instrumentId")


class FundingRateSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    FundingRate: FundingRateSubscriptionFields


class InstrumentStatsSubscriptionFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: InstrumentId = Field(alias="instrumentId")


class InstrumentStatsSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    InstrumentStats: InstrumentStatsSubscriptionFields


class CandleSubscriptionFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: InstrumentId = Field(alias="instrumentId")
    interval: CandleTimeframe


class CandleSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    Candle: CandleSubscriptionFields


class PositionFundingSubscriptionFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    account: AccountAddress


class PositionFundingSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    PositionFunding: PositionFundingSubscriptionFields


class LastMatchPriceSubscriptionFields(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: InstrumentId = Field(alias="instrumentId")


class LastMatchPriceSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    LastMatchPrice: LastMatchPriceSubscriptionFields


SubscriptionKind = (
    OrderbookSubscription
    | PriceFeedSubscription
    | AssetPriceFeedSubscription
    | OrderEventsSubscription
    | CollateralSubscription
    | PositionSubscription
    | AccountRiskSubscription
    | OpenOrdersSubscription
    | FundingRateSubscription
    | InstrumentStatsSubscription
    | CandleSubscription
    | PositionFundingSubscription
    | LastMatchPriceSubscription
)


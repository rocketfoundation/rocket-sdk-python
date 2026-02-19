from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from rocket_sdk_python.types.primitives import AccountAddress, AssetId, InstrumentId
from rocket_sdk_python.types.rest.candles import CandleTimeframe


class OrderbookSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["Orderbook"] = "Orderbook"
    instrument_id: InstrumentId = Field(alias="instrumentId")


class PriceFeedSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["PriceFeed"] = "PriceFeed"
    instrument_id: InstrumentId = Field(alias="instrumentId")


class AssetPriceFeedSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["AssetPriceFeed"] = "AssetPriceFeed"
    asset_id: AssetId = Field(alias="assetId")


class OrderEventsSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["OrderEvents"] = "OrderEvents"
    account: AccountAddress | None = None
    instrument_id: InstrumentId | None = Field(default=None, alias="instrumentId")


class CollateralSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["Collateral"] = "Collateral"
    asset_id: AssetId = Field(alias="assetId")
    account: AccountAddress


class PositionSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["Position"] = "Position"
    account: AccountAddress


class AccountRiskSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["AccountRisk"] = "AccountRisk"
    account: AccountAddress


class OpenOrdersSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["OpenOrders"] = "OpenOrders"
    account: AccountAddress


class FundingRateSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["FundingRate"] = "FundingRate"
    instrument_id: InstrumentId = Field(alias="instrumentId")


class InstrumentStatsSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["InstrumentStats"] = "InstrumentStats"
    instrument_id: InstrumentId = Field(alias="instrumentId")


class CandleSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["Candle"] = "Candle"
    instrument_id: InstrumentId = Field(alias="instrumentId")
    interval: CandleTimeframe


class PositionFundingSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["PositionFunding"] = "PositionFunding"
    account: AccountAddress


class LastMatchPriceSubscription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Literal["LastMatchPrice"] = "LastMatchPrice"
    instrument_id: InstrumentId = Field(alias="instrumentId")


SubscriptionKind = Annotated[
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
    | LastMatchPriceSubscription,
    Field(discriminator="type"),
]


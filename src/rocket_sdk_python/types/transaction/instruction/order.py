from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, SerializationInfo, model_serializer

from rocket_sdk_python.types.primitives import (
    AccountAddress,
    GlobalOrderId,
    InstrumentId,
    MMPTag,
    OrderSide,
)

MAX_ORDER_REQUESTS_PER_TRANSACTION = 100


def _omit_none_if_human_readable(
    data: dict[str, Any], keys: tuple[str, ...], info: SerializationInfo
) -> dict[str, Any]:
    context = info.context or {}
    if "human_readable" in context:
        human = bool(context["human_readable"])
    else:
        human = info.mode == "json"
    if not human:
        return data
    for key in keys:
        if data.get(key) is None:
            data.pop(key, None)
    return data


class ContractTypeFilter(str, Enum):
    PERP = "perp"
    OPTION = "option"


class PlaceLimitOrderRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: InstrumentId = Field(alias="instrumentId")
    side: OrderSide
    price: str
    quantity: str
    trader: AccountAddress
    trigger_price: str | None = Field(default=None, alias="triggerPrice")
    reduce_only: bool = Field(alias="reduceOnly")
    take_profit: bool = Field(alias="takeProfit")
    mmp_tag: MMPTag | None = Field(default=None, alias="mmpTag")

    @model_serializer(mode="wrap")
    def _serialize(self, serializer: Any, info: SerializationInfo) -> Any:
        data = serializer(self)
        if isinstance(data, dict):
            return _omit_none_if_human_readable(data, ("mmpTag",), info)
        return data


class PlaceMarketOrderRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: InstrumentId = Field(alias="instrumentId")
    side: OrderSide
    quantity: str
    trader: AccountAddress
    trigger_price: str | None = Field(default=None, alias="triggerPrice")
    reduce_only: bool = Field(alias="reduceOnly")
    take_profit: bool = Field(alias="takeProfit")
    max_slippage: str | None = Field(default=None, alias="maxSlippage")
    mmp_tag: MMPTag | None = Field(default=None, alias="mmpTag")

    @model_serializer(mode="wrap")
    def _serialize(self, serializer: Any, info: SerializationInfo) -> Any:
        data = serializer(self)
        if isinstance(data, dict):
            return _omit_none_if_human_readable(data, ("mmpTag",), info)
        return data


class PlaceTWAPRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: InstrumentId = Field(alias="instrumentId")
    side: OrderSide
    quantity: str
    trader: AccountAddress
    max_slippage: str | None = Field(default=None, alias="maxSlippage")
    reduce_only: bool = Field(alias="reduceOnly")
    twap_interval: int = Field(alias="twapInterval")
    frequency: int | None = None
    randomize: bool | None = None
    mmp_tag: MMPTag | None = Field(default=None, alias="mmpTag")

    @model_serializer(mode="wrap")
    def _serialize(self, serializer: Any, info: SerializationInfo) -> Any:
        data = serializer(self)
        if isinstance(data, dict):
            return _omit_none_if_human_readable(data, ("mmpTag",), info)
        return data


class ModifyTWAPRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    order_id: GlobalOrderId = Field(alias="orderId")
    trader: AccountAddress
    new_twap_interval: int | None = Field(default=None, alias="newTwapInterval")
    new_quantity: str | None = Field(default=None, alias="newQuantity")
    new_frequency: int | None = Field(default=None, alias="newFrequency")
    new_randomize: bool | None = Field(default=None, alias="newRandomize")


class CancelOrderRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    order_id: GlobalOrderId = Field(alias="orderId")
    trader: AccountAddress


class CancelAllOrderRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    instrument_id: InstrumentId | None = Field(default=None, alias="instrumentId")
    trader: AccountAddress
    underlying: str | None = None
    contract_type: ContractTypeFilter | None = Field(default=None, alias="contractType")
    delta_lower: str | None = Field(default=None, alias="deltaLower")
    delta_upper: str | None = Field(default=None, alias="deltaUpper")

    @model_serializer(mode="wrap")
    def _serialize(self, serializer: Any, info: SerializationInfo) -> Any:
        data = serializer(self)
        if isinstance(data, dict):
            return _omit_none_if_human_readable(
                data,
                ("underlying", "contractType", "deltaLower", "deltaUpper"),
                info,
            )
        return data


class ModifyOrderRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    order_id: GlobalOrderId = Field(alias="orderId")
    new_price: str = Field(alias="newPrice")
    trader: AccountAddress
    new_quantity: str = Field(alias="newQuantity")
    new_trigger_price: str | None = Field(default=None, alias="newTriggerPrice")


class LimitOrder(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    Limit: PlaceLimitOrderRequest


class MarketOrder(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    Market: PlaceMarketOrderRequest


class CancelOrder(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    Cancel: CancelOrderRequest


class CancelAllOrder(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    CancelAll: CancelAllOrderRequest


class ModifyOrder(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    Modify: ModifyOrderRequest


OrderRequest = LimitOrder | MarketOrder | CancelOrder | CancelAllOrder | ModifyOrder

OrderRequestSet = list[OrderRequest]


class PlaceOrderInstruction(BaseModel):
    PlaceOrder: OrderRequestSet


class PlaceTWAPInstruction(BaseModel):
    PlaceTWAP: PlaceTWAPRequest


class ModifyTWAPInstruction(BaseModel):
    ModifyTWAP: ModifyTWAPRequest

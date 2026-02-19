from typing import Annotated

from pydantic import AfterValidator, BeforeValidator

Signature = Annotated[
    str,
    BeforeValidator(lambda v: v if isinstance(v, str) else str(v)),
    AfterValidator(lambda v: v if v.startswith("0x") else f"0x{v}"),
]

InstrumentId = int

AssetId = int

GlobalOrderId = int

BlockTimestamp = int

Shares = int

Round = int

OrderIx = int

AssetTicker = str

HaircutTick = int

PriceScale = int

PriceTick = int

QuantityScale = int

QuantityTick = int

FeeRate = int

TradedVolume = int

ScenarioChange = int

InstrumentFlags = int

PnLTick = int

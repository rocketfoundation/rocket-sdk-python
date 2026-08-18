from enum import Enum


class AggregatedInstrumentType(str, Enum):
    SPOT = "Spot"
    PERPETUALS = "Perpetuals"
    FUTURES = "Futures"
    OPTIONS = "Options"
    UNKNOWN = "Unknown"

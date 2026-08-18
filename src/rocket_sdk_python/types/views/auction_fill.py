from pydantic import BaseModel, ConfigDict

from rocket_sdk_python.types.primitives import BlockTimestamp


class AuctionFillView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    price: str
    size: str
    timestamp: BlockTimestamp


class AuctionFillEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    size: str
    timestamp: BlockTimestamp

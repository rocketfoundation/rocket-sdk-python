from pydantic import BaseModel, ConfigDict, Field


class QuoteView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    timestamp: int
    bid_price: str = Field(alias="bidPrice")
    bid_size: str = Field(alias="bidSize")
    ask_price: str = Field(alias="askPrice")
    ask_size: str = Field(alias="askSize")


class TickerView(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    timestamp: int = Field(alias="t")
    ask_size: str | None = Field(default=None, alias="A")
    ask_price: str | None = Field(default=None, alias="a")
    bid_size: str | None = Field(default=None, alias="B")
    bid_price: str | None = Field(default=None, alias="b")
    mark_price: str | None = Field(default=None, alias="I")
    mid_price: str | None = Field(default=None, alias="M")
    iv: str | None = Field(default=None, alias="V")
    delta: str | None = Field(default=None, alias="D")
    gamma: str | None = Field(default=None, alias="G")
    theta: str | None = Field(default=None, alias="H")
    vega: str | None = Field(default=None, alias="e")
    rho: str | None = Field(default=None, alias="R")

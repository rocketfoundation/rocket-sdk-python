from enum import Enum


class OrderSide(str, Enum):
    BUY = "Buy"
    SELL = "Sell"

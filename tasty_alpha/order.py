from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from .asset import Asset
from .exchange import Exchange
from .market import Market
from .utils import utc_now

class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"

class OrderStatus(Enum):
    LOCAL = "_local"
    PENDING = "pending"
    OPEN = "open"
    REJECTED = "rejected"
    CANCELED = "canceled"

class OrderSide(Enum):
    SELL = 1 << 0
    BUY = 1 << 1

def default_exchange():
    return Exchange.default()

@dataclass
class Order:
    market: Market
    amount: float
    side: int
    type: OrderType
    price: Optional[float] = None
    status: OrderStatus = OrderStatus.LOCAL
    exchange: Exchange = field(default_factory=default_exchange)
    timestamp: datetime = field(default_factory=utc_now)

@dataclass
class LimitOrder(Order):
    type: OrderType = OrderType.LIMIT

@dataclass
class MarketOrder(Order):
    type: OrderType = OrderType.MARKET


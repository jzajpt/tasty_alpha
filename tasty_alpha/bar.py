from aiopubsub import Key
from .trade import Trade

class Bar:
    def __init__(self, first_trade: Trade) -> None:
        self.time = first_trade.timestamp
        self.open = first_trade.price
        self.high = first_trade.price
        self.low = first_trade.price
        self.close = first_trade.price
        self.volume = first_trade.amount
        self.dollar_value = first_trade.price * first_trade.amount
        self.count = 1

    def __str__(self) -> None:
        return f"[{self.open}, {self.high}, {self.low}, {self.close}] {self.count}"

    def to_dict(self) -> None:
        return {
            'time': self.time,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'volume': self.volume,
            'dollar_value': self.dollar_value,
            'count': self.count,
        }

    def on_new_trade(self, key: Key, trade: Trade) -> None:
        if self.count == 0:
            self.open = trade.price
        if not self.high or trade.price > self.high:
            self.high = trade.price
        if not self.low or trade.price < self.low:
            self.low = trade.price
        self.close = trade.price
        self.dollar_value += trade.dollar_value
        self.count += 1


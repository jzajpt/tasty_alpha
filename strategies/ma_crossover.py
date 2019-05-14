import aiopubsub
from loguru import logger
import numpy as np
from tasty_alpha.broker import Broker
from tasty_alpha.exchange import Exchanges
from tasty_alpha.market import Markets
from tasty_alpha.order import LimitOrder, MarketOrder, OrderSide
from tasty_alpha.sampling.bar import Bar
from tasty_alpha.strategy import Strategy

class MACrossStrategy(Strategy):
    exchange = Exchanges.Kraken
    market = Markets.BTCUSD

    def __init__(self,
                 hub: aiopubsub.Hub,
                 broker: Broker,
                 p1: int = 20,
                 p2: int = 80) -> None:
        super().__init__(hub, broker)
        if p1 >= p2:
            raise Exception("p1 has to be smaller than p2")
        self.p1 = p1
        self.p2 = p2

    def __call__(self, bar: Bar) -> None:
        if len(self.bars) < self.p2:
            return

        long_ma = self.mean_open(self.p2)
        short_ma = self.mean_open(self.p1)
        if short_ma > long_ma and not self.position_manager.is_open:
            buy_order = LimitOrder(self.market,
                                   amount=1.0,
                                   side=OrderSide.BUY,
                                   price=bar.close)
            self.broker.submit_order(buy_order)
        elif short_ma <= long_ma and self.position_manager.is_open:
            self.position_manager.close_position(bar.close)

    def mean_open(self, window):
        open_prices = [bar.open for bar in self.bars[-window:]]
        return np.mean(open_prices)


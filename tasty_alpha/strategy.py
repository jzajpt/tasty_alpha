from aiopubsub import Key, Hub, Subscriber
from loguru import logger
import numpy as np
from .market import Market
from .position_manager import PositionManager
from .sampling.bar import Bar

class Strategy:
    """
    A single market strategy.
    """

    def __init__(self, hub: Hub, exchange: str, market: Market) -> None:
        self.subscriber = Subscriber(hub, 'strategy')
        bar_key = Key('*', f"{exchange}-{market}", 'new-bar')
        self.subscriber.add_sync_listener(bar_key, self.store_new_bar)
        self.subscriber.add_sync_listener(bar_key, self.on_new_bar)
        self.position_manager = PositionManager(market)
        self.bars = []

    def store_new_bar(self, key: Key, bar: Bar) -> None:
        self.bars.append(bar)

    def on_new_bar(self, key: Key, bar: Bar) -> None:
        pass


class MovingAverageCrossStrategy(Strategy):
    def on_new_bar(self, key: Key, bar: Bar):
        if len(self.bars) < 80:
            return

        long_ma = self.mean_open(80)
        short_ma = self.mean_open(20)
        if short_ma > long_ma and not self.position_manager.is_open:
            self.position_manager.open_position(1.0, bar.close)
            logger.info("{short_ma} > {long_ma}", short_ma=short_ma, long_ma=long_ma)
        elif short_ma <= long_ma and self.position_manager.is_open:
            self.position_manager.close_position(bar.close)

            if len(self.position_manager.past_positions) > 10:
                realized_pnl = self.position_manager.total_realized_pnl()
                logger.info("Total return so far = {total}",
                        total=realized_pnl)

    def mean_open(self, window):
        open_prices = [bar.open for bar in self.bars[-window:]]
        return np.mean(open_prices)


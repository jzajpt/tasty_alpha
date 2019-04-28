import aiopubsub
from loguru import logger
import numpy as np
from tasty_alpha.exchange import Exchanges
from tasty_alpha.market import Markets
from tasty_alpha.sampling.bar import Bar
from tasty_alpha.strategy import Strategy

class MACrossStrategy(Strategy):
    exchange = Exchanges.Kraken
    market = Markets.BTCUSD

    def on_new_bar(self, key: aiopubsub.Key, bar: Bar):
        print(bar.time)
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


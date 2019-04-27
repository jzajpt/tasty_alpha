from aiopubsub import Hub, Publisher, Subscriber, Key
from loguru import logger
import numpy as np
from pyti.exponential_moving_average import exponential_moving_average as ema
from ..trade import Trade
from .bar import Bar
from .. import events

class ImbalanceBarGenerator:
    def _build_new_bar(self, trade: Trade, namespace: str) -> Bar:
        self.publisher.publish([namespace, 'new-bar'], self.bar)
        self.bar = Bar(trade)

class TickImbalanceBarGenerator(ImbalanceBarGenerator):
    """
    Tick imbalance bars (TIBs) are produced more frequently when there is
    informed trading (asymmetric information).

    Attributes:
    last_trade (Trade): the last observed trade
    b_ts (List[int]): the sign of the price change between ticks
    theta (int): current tick imbalance
    expected_theta (int): expected tick imbalance
    """

    def __init__(self, hub: Hub, initial_theta: int = 50) -> None:
        self.subscriber = Subscriber(hub, 'tick_imbalance_bar_generator')
        self.subscriber.add_sync_listener(events.AnyNewTrade, self.on_new_trade)
        self.publisher = Publisher(hub, prefix='tick_imbalance_bar_generator')
        self.bar = None
        self.last_trade = None
        self.b_ts = []
        self.t_vals = []
        self.theta = 0
        self.expected_theta = initial_theta
        self.initial_T = 50

    def price_change(self, trade: Trade) -> int:
        if self.last_trade:
            return np.sign(trade.price - self.last_trade.price)
        else:
            return 0

    def on_new_trade(self, key: Key, trade: Trade) -> None:
        if not self.bar:
            self.bar = Bar(trade)
        b_t = self.price_change(trade)
        self.b_ts.append(b_t)
        self.theta += b_t
        self.bar.append(trade)
        self.last_trade = trade
        if np.abs(self.theta) >= np.abs(self.expected_theta):
            self.t_vals.append(self.bar.count)
            window = 5
            if len(self.t_vals) > window:
                expected_T = ema(self.t_vals, window)[-1]
            else:
                expected_T = self.t_vals[-1]
            namespace = key[1]
            self._build_new_bar(trade, namespace)
            self.theta = 0
            logger.info(f"Expected T: {expected_T}")
            # print(ema(self.b_ts, 10))
            probability = ema(self.b_ts, 10)[-1]
            self.expected_theta = expected_T * (2 * probability - 1)
            logger.info(self.expected_theta)


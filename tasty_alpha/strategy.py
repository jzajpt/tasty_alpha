from aiopubsub import Key, Hub, Subscriber
from loguru import logger
import numpy as np
from .exchange import Exchanges
from .market import Market, Markets
from .position_manager import PositionManager
from .sampling.bar import Bar

class Strategy:
    """
    A single market strategy.
    """
    exchange = None
    market = None

    def __init__(self, hub: Hub) -> None:
        self.subscriber = Subscriber(hub, 'strategy')
        bar_key = Key('*', f"{self.exchange}-{self.market}", 'new-bar')
        self.subscriber.add_sync_listener(bar_key, self.store_new_bar)
        self.subscriber.add_sync_listener(bar_key, self.on_new_bar)
        self.position_manager = PositionManager(self.market)
        self.bars = []

    def store_new_bar(self, key: Key, bar: Bar) -> None:
        self.bars.append(bar)

    def on_new_bar(self, key: Key, bar: Bar) -> None:
        pass


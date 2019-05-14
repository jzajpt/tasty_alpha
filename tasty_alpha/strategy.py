from aiopubsub import Key, Hub, Subscriber
from loguru import logger
import numpy as np
import re
import runpy
from .broker import Broker
from .market import Market, Markets
from .position_manager import PositionManager
from .sampling.bar import Bar

def read_strategy_name(file: str):
    with open(file, 'r') as f:
        strategy_file = f.read()
        match = re.search("class (.+)\(Strategy\):", strategy_file)
        if match:
            return match[1]

def read_and_run_strategy_file(file: str):
    strategy_name = read_strategy_name(file)
    strategy_code = runpy.run_path(file)
    return strategy_code[strategy_name]

class Strategy:
    """
    MutliStrategy is a base class for strategies that need to operate on a
    single market.
    """
    exchange = None
    market = None

    def __init__(self, hub: Hub, broker: Broker) -> None:
        self.subscriber = Subscriber(hub, 'strategy')
        bar_key = Key('*', f"{self.exchange}-{self.market}", 'new-bar')
        self.subscriber.add_sync_listener(bar_key, self.store_new_bar)
        self.subscriber.add_sync_listener(bar_key, self.on_new_bar)
        self.position_manager = PositionManager(hub, self.market)
        self.broker = broker
        self.bars = []

    def __call__(self, bar: Bar):
        pass

    def store_new_bar(self, key: Key, bar: Bar) -> None:
        self.bars.append(bar)

    def on_new_bar(self, key: Key, bar: Bar) -> None:
        self.__call__(bar)

class MultiStrategy:
    """
    MutliStrategy is a base class for strategies that need to take in
    information from multiple markets.
    """
    pairs = []

    def __init__(self, hub: Hub, broker: Broker) -> None:
        self.subscriber = Subscriber(hub, 'multi_strategy')
        for pair in self.pairs:
            namespace = f"{pair[0]}-{pair[1]}"
            bar_key = Key('*', namespace, 'new-bar')
            self.subscriber.add_sync_listener(bar_key, self.store_new_bar)
            self.subscriber.add_sync_listener(bar_key, self.on_new_bar)
        self.broker = broker
        self.bars = {}

    def store_new_bar(self, key: Key, bar: Bar) -> None:
        namespace = key[1]
        if namespace not in self.bars:
            self.bars[namespace] = []
        self.bars[namespace].append(bar)

    def on_new_bar(self, key: Key, bar: Bar) -> None:
        pass


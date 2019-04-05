from aiopubsub import Key, Hub, Subscriber
from loguru import logger
from . import events
from .sampling.bar import Bar

class Strategy:
    def __init__(self, hub: Hub) -> None:
        self.subscriber = Subscriber(hub, 'strategy')
        self.subscriber.add_sync_listener(events.AnyNewBar, self.on_new_bar)

    def on_new_bar(self, key: Key, bar: Bar):
        pass

class MovingAverageCrossStrategy(Strategy):
    def on_new_bar(self, key: Key, bar: Bar):
        logger.info("Bar = {bar}", bar=bar)


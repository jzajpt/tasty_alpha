import asyncio
from aiopubsub import Hub, Publisher, Subscriber, Key
from typing import Union
from ..trade import Trade
from .bar import Bar
from .. import events

class ThresholdBarGenerator:
    def __init__(self, hub: Hub, threshold: int):
        self.subscriber = Subscriber(hub, 'threshold_bars')
        self.subscriber.add_sync_listener(events.AnyNewTrade, self.on_new_trade)
        self.publisher = Publisher(hub, prefix='threshold_bars')
        self.threshold = threshold
        self.bar = None
        self.value = 0

    def on_new_trade(self, key: Key, trade: Trade) -> None:
        if not self.bar:
            self.bar = Bar(trade)
        self.bar.on_new_trade(key, trade)
        if self.value > self.threshold:
            self._build_new_bar(trade)
        self.value += self.metric(trade)

    def _build_new_bar(self, trade: Trade) -> Bar:
        self.value = 0
        self.publisher.publish(events.NewBar, self.bar)
        self.bar = Bar(trade)


class TickBarGenerator(ThresholdBarGenerator):
    def metric(self, trade: Trade) -> float:
        return 1

class VolumeBarGenerator(ThresholdBarGenerator):
    def metric(self, trade: Trade) -> float:
        return trade.amount

class DollarBarGenerator(ThresholdBarGenerator):
    def metric(self, trade: Trade) -> float:
        return trade.dollar_value

PossibleBarTypes = Union[TickBarGenerator, DollarBarGenerator, VolumeBarGenerator]

def new_bar_generator(bar: str,
        hub: Hub,
        threshold: int
        ) -> PossibleBarTypes:
    if bar == 'tick':
        return TickBarGenerator(hub, threshold)
    elif bar == 'dollar' or bar == 'base':
        return  DollarBarGenerator(hub, threshold)
    elif bar == 'volume':
        return  VolumeBarGenerator(hub, threshold)
    else:
        raise Exception(f'Invalid bar generator type: {bar}')


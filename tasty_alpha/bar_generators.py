import asyncio
from aiopubsub import Hub, Publisher, Subscriber, Key
from typing import Union
from .bar import Bar

class ThresholdBarGenerator:
    def __init__(self, hub: Hub, threshold: int):
        self.subscriber = Subscriber(hub, 'threshold_bars')
        self.new_trade_key = Key('*', 'new-trade')
        self.subscriber.add_sync_listener(self.new_trade_key, self.on_new_trade)
        self.publisher = Publisher(hub, prefix='threshold_bars')
        self.threshold = threshold
        self.bar = None
        self.value = 0

    def _build_new_bar(self, trade) -> None:
        if self.bar:
            self.subscriber.remove_listener(self.new_trade_key,
                    self.bar.on_new_trade)
        self.bar = Bar(trade)
        self.subscriber.add_sync_listener(self.new_trade_key,
                self.bar.on_new_trade)

    def on_new_trade(self, key, trade) -> None:
        if not self.bar:
            self.bar = Bar(trade)
        if self.value > self.threshold:
            self.value = 0
            processing_finished_key = Key('processing-finished')
            self.publisher.publish(processing_finished_key, '')
            new_bar_key = Key('new-bar')
            self.publisher.publish(new_bar_key, self.bar)
            self._build_new_bar(trade)
        self.value += self.metric(trade)

class TickBarGenerator(ThresholdBarGenerator):
    def metric(self, trade):
        return 1

class VolumeBarGenerator(ThresholdBarGenerator):
    def metric(self, trade):
        return trade.amount

class DollarBarGenerator(ThresholdBarGenerator):
    def metric(self, trade):
        return trade.amount * trade.price

PossibleBarTypes = Union[TickBarGenerator, DollarBarGenerator, VolumeBarGenerator]

import pytest
from aiopubsub import Hub, Publisher, Subscriber, Key
from tasty_alpha.trade import Trade
from tasty_alpha import events
from tasty_alpha.sampling.bar_generators import TickBarGenerator, \
    VolumeBarGenerator, DollarBarGenerator

def test_tick_bar_generation_after_threshold():
    hub = Hub()
    publisher = Publisher(hub, 'test-publisher')
    generator = TickBarGenerator(hub, threshold=3)
    subscriber = Subscriber(hub, 'test-subscriber')
    bars = []
    def new_bar_handler(key, bar):
        bars.append(bar)
    subscriber.add_sync_listener(events.AnyNewBar, new_bar_handler)
    assert len(bars) == 0
    for i in range(5):
        trade = Trade(12345, price=1.0, amount=1.0)
        publisher.publish(events.NewTrade, trade)
    assert len(bars) == 1


def test_volume_bar_generation_after_threshold():
    hub = Hub()
    publisher = Publisher(hub, 'test-publisher')
    generator = VolumeBarGenerator(hub, threshold=2.0)
    subscriber = Subscriber(hub, 'test-subscriber')
    bars = []
    def new_bar_handler(key, bar):
        bars.append(bar)
    subscriber.add_sync_listener(events.AnyNewBar, new_bar_handler)
    assert len(bars) == 0
    for i in range(6):
        trade = Trade(12345, price=1.0, amount=1.0)
        publisher.publish(events.NewTrade, trade)
    assert len(bars) == 2


def test_dollar_bar_generation_after_threshold():
    hub = Hub()
    publisher = Publisher(hub, 'test-publisher')
    generator = DollarBarGenerator(hub, threshold=2.0)
    subscriber = Subscriber(hub, 'test-subscriber')
    bars = []
    def new_bar_handler(key, bar):
        bars.append(bar)
    subscriber.add_sync_listener(events.AnyNewBar, new_bar_handler)
    assert len(bars) == 0
    for i in range(5):
        trade = Trade(12345, price=0.5, amount=1.0)
        publisher.publish(events.NewTrade, trade)
    assert len(bars) == 1


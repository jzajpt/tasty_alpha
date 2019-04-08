import pytest
from aiopubsub import Hub, Publisher
from tasty_alpha.strategy import Strategy

class NewBarTestStrategy(Strategy):
    def on_new_bar(self, key, bar):
        self.on_new_bar_called = True

def test_strategy_on_new_bar_is_called():
    hub = Hub()
    publisher = Publisher(hub, 'test-publisher')
    bar = None
    strat = NewBarTestStrategy(hub)
    publisher.publish('new-bar', bar)
    assert strat.on_new_bar_called

def test_strategy_stores_bars():
    hub = Hub()
    publisher = Publisher(hub, 'test-publisher')
    bars = [1, 2, 3]
    strat = NewBarTestStrategy(hub)
    [publisher.publish('new-bar', bar) for bar in bars]
    assert strat.bars == bars





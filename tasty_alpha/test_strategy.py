import pytest
from aiopubsub import Hub, Publisher
from tasty_alpha.asset import Asset
from tasty_alpha.market import Markets
from tasty_alpha.strategy import Strategy, MovingAverageCrossStrategy
from tasty_alpha.trade import Trade
from tasty_alpha.sampling.bar import Bar

class NewBarTestStrategy(Strategy):
    def on_new_bar(self, key, bar):
        self.on_new_bar_called = True

def test_strategy_on_new_bar_is_called():
    hub = Hub()
    publisher = Publisher(hub, 'test-publisher')
    trade = Trade(12345, price=1.0, amount=1.0)
    bar = Bar(trade)
    exchange = 'test'
    market = Markets.BTCUSD
    strat = NewBarTestStrategy(hub, exchange, market)
    publisher.publish([f'{exchange}-{market}', 'new-bar'], bar)
    assert strat.on_new_bar_called

def test_strategy_stores_bars():
    hub = Hub()
    publisher = Publisher(hub, 'test-publisher')
    bars = [1, 2, 3]
    exchange = 'test'
    market = Markets.BTCUSD
    strat = NewBarTestStrategy(hub, exchange, market)
    [publisher.publish([f'{exchange}-{market}', 'new-bar'], bar) for bar in bars]
    assert strat.bars == bars

def test_moving_average_cross_strategy_mean_open():
    hub = Hub()
    publisher = Publisher(hub, 'test-publisher')
    exchange = 'test'
    market = Markets.BTCUSD
    strat = MovingAverageCrossStrategy(hub, exchange, market)
    for i in range(100):
        trade = Trade(12345, price=1.0, amount=1.0)
        bar = Bar(trade)
        publisher.publish([f'{exchange}-{market}', 'new-bar'], bar)
    assert strat.mean_open(50) == 1.0

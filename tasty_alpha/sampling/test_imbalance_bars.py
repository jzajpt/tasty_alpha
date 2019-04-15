import pytest
import numpy as np
from aiopubsub import Hub, Publisher, Subscriber, Key
from tasty_alpha.trade import Trade
from tasty_alpha import events
from tasty_alpha.sampling.imbalance_bars import TickImbalanceBarGenerator

@pytest.fixture
def hub():
    return Hub()

@pytest.fixture
def publisher(hub):
    return Publisher(hub, 'test-publisher')

@pytest.fixture
def subscriber(hub):
    return Subscriber(hub, 'test-subscriber')

@pytest.fixture
def tib_generator(hub):
    return TickImbalanceBarGenerator(hub)

def test_tib_bar_generation_tb_sequence(publisher, tib_generator):
    for i in range(5):
        trade = Trade(12345, price=1.0 + i, amount=1.0)
        publisher.publish(events.NewTrade, trade)
    assert len(tib_generator.b_ts) == 5
    assert tib_generator.b_ts == [0.0, 1.0, 1.0, 1.0, 1.0]
    assert tib_generator.theta == 4

def test_tib_bar_generation_tb_sequence(publisher, tib_generator):
    for i in range(5):
        trade = Trade(12345, price=10.0 - i, amount=1.0)
        publisher.publish(events.NewTrade, trade)
    assert len(tib_generator.b_ts) == 5
    assert tib_generator.b_ts == [0.0, -1.0, -1.0, -1.0, -1.0]
    assert tib_generator.theta == -4

def test_tib_bar_generation_generates(publisher, subscriber, hub):
    bars = []
    def new_bar_handler(key, bar):
        bars.append(bar)
    subscriber.add_sync_listener(events.AnyNewBar, new_bar_handler)
    tib_generator = TickImbalanceBarGenerator(hub, initial_theta=10)
    n = 100
    for p in np.random.normal(scale=0.1,size=n) + np.linspace(1, 20, n):
        trade = Trade(12345, price=p, amount=1.0)
        publisher.publish(events.NewTrade, trade)
    assert len(bars) == 1


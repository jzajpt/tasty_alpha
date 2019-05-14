import aiopubsub
import pytest
from tasty_alpha.asset import Asset
from tasty_alpha.broker import BacktestBroker

@pytest.fixture
def backtest_broker():
    hub = aiopubsub.Hub()
    return BacktestBroker(hub)

def test_submit_order(backtest_broker, order):
    position = backtest_broker.submit_order(order)
    assert len(backtest_broker.orders) == 1


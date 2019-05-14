import pytest
from aiopubsub import Hub, Publisher
from tasty_alpha.asset import Asset
from tasty_alpha.market import Market, Markets
from tasty_alpha.order import Order, OrderSide, OrderType
from tasty_alpha.position import Position

@pytest.fixture(scope="module")
def hub() -> Hub:
    return Hub()

@pytest.fixture(scope="module")
def publisher(hub) -> Publisher:
    return Publisher(hub, 'test_publisher')

@pytest.fixture(scope="module")
def market() -> Market:
    return Markets.BTCUSD

@pytest.fixture(scope="module")
def order(market) -> Order:
    return Order(Markets.BTCUSD, 1.0, OrderSide.BUY, OrderType.MARKET, 5555.123)

@pytest.fixture(scope="module")
def position(amount = 1.0, ticker = "BTC"):
    asset = Asset(ticker)
    return Position(asset, amount)


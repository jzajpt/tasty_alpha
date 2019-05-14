import pytest
from tasty_alpha.market import Market, Markets
from tasty_alpha.order import Order, OrderSide, OrderType

@pytest.fixture(scope="module")
def market() -> Market:
    return Markets.BTCUSD

@pytest.fixture(scope="module")
def order(market) -> Order:
    return Order(Markets.BTCUSD, 1.0, OrderSide.BUY, OrderType.MARKET, 5555.123)


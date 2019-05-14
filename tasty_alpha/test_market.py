import pytest
from tasty_alpha.market import Market, Markets

def test_market_str():
    assert str(Markets.BTCUSD) == "BTCUSD"

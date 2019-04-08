import pytest
from tasty_alpha.trade import Trade

def test_trade_dollar_value():
    trade = Trade(1, 1.0, 2.0)
    assert trade.dollar_value == 2.0


import pytest
from tasty_alpha.trade import Trade
from tasty_alpha.sampling.bar import Bar

def test_bar_initial_attrs_from_trade():
    trade = Trade(123456, 3.0, 1.5)
    bar = Bar(trade)
    assert bar.dollar_value == trade.dollar_value
    assert bar.time == trade.timestamp
    assert bar.open == trade.price
    assert bar.high == trade.price
    assert bar.low == trade.price
    assert bar.close == trade.price
    assert bar.count == 1

def test_bar_append_new_high():
    trade_1 = Trade(123456, price=3.0, amount=1.0)
    trade_2 = Trade(123456, price=3.1, amount=1.0)
    trade_3 = Trade(123456, price=3.0, amount=1.0)
    bar = Bar(trade_1)
    bar.append(trade_2)
    bar.append(trade_3)
    assert bar.high == trade_2.price

def test_bar_append_new_low():
    trade_1 = Trade(123456, price=3.0, amount=1.0)
    trade_2 = Trade(123456, price=2.9, amount=1.0)
    trade_3 = Trade(123456, price=3.1, amount=1.0)
    bar = Bar(trade_1)
    bar.append(trade_2)
    bar.append(trade_3)
    assert bar.low == trade_2.price

def test_bar_append_does_not_change_open():
    trade_1 = Trade(123456, price=3.0, amount=1.0)
    trade_2 = Trade(123456, price=2.9, amount=1.0)
    bar = Bar(trade_1)
    bar.append(trade_2)
    assert bar.open == trade_1.price

def test_bar_append_changes_close():
    trade_1 = Trade(123456, price=3.0, amount=1.0)
    trade_2 = Trade(123456, price=2.9, amount=1.0)
    bar = Bar(trade_1)
    bar.append(trade_2)
    assert bar.close == trade_2.price

def test_bar_append_increases_count():
    trade_1 = Trade(123456, price=3.0, amount=1.0)
    trade_2 = Trade(123456, price=2.9, amount=1.0)
    bar = Bar(trade_1)
    bar.append(trade_2)
    assert bar.count == 2

def test_bar_append_increases_volume():
    trade_1 = Trade(123456, price=3.0, amount=1.0)
    trade_2 = Trade(123456, price=2.9, amount=1.0)
    bar = Bar(trade_1)
    bar.append(trade_2)
    assert bar.volume == (trade_1.amount + trade_2.amount)

def test_bar_append_increases_dollar_value():
    trade_1 = Trade(123456, price=3.0, amount=1.0)
    trade_2 = Trade(123456, price=2.9, amount=1.0)
    bar = Bar(trade_1)
    bar.append(trade_2)
    assert bar.dollar_value == (trade_1.dollar_value + trade_2.dollar_value)


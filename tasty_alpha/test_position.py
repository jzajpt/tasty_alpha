import pytest
from tasty_alpha.asset import Asset
from tasty_alpha.position import Position, PositionStatus

def test_new_position_timestamp(position):
    assert position.timestamp

def test_new_position_status(position):
    assert position.status == PositionStatus.Pending

def test_position_open_calculates_cost(position):
    position.open(price=1000.0, fees=5.0)
    assert position.cost == 1005.0
    assert position.status == PositionStatus.Open

def test_position_close_calculates_realized_pnl(position):
    """
    Assume buying price 1000.0 and selling price 1005.0 with no fees
    """
    position.open(price=1000.0, fees=0.0)
    position.close(price=1005.0, fees=0.0)
    assert position.realized_pnl == 5.0
    assert position.status == PositionStatus.Closed

def test_position_close_calculates_realized_pnl_with_fees(position):
    """
    Assume buying price 1000.0 and selling price 1008.5 with fees of 0.05%.
    """
    position.open(price=1000.0, fees=5.0) # cost = 1005
    position.close(price=1008.5, fees=5.0425)
    assert position.realized_pnl == ((1008.5 - 5.0425) - 1005.0)
    assert position.status == PositionStatus.Closed
    assert position.closed_at

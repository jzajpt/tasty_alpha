import pytest
from tasty_alpha.order import Order, OrderStatus

def test_order_timestamp_has_default(order):
    assert order.timestamp

def test_order_status_is_local_default(order):
    assert order.status == OrderStatus.LOCAL


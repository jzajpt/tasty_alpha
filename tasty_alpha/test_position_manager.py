import pytest
from aiopubsub import Publisher
from tasty_alpha.position import Position, PositionStatus
from tasty_alpha.position_manager import PositionManager

@pytest.fixture
def position_manager(hub, market):
    return PositionManager(hub, market)

def test_position_manager_is_open_without_position(position_manager):
    assert not position_manager.is_open

def test_position_manager_is_open_after_new_position(publisher,
                                                     position_manager,
                                                     position):
    publisher.publish(['BTCUSD', 'new-position'], position)
    assert position_manager.is_open


def test_position_manager_close_position(publisher,
                                         position_manager,
                                         position):
    position.open(price=5555)
    publisher.publish(['BTCUSD', 'new-position'], position)
    position_manager.close_position(position.cost + 0.1)
    assert position.status == PositionStatus.Closed
    assert not position_manager.is_open



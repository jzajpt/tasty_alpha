from aiopubsub import Key, Hub, Publisher, Subscriber
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from . import events
from .exchange import Exchange
from .market import Market
from .position import Position
from .order import Order, OrderType, OrderSide
from .trade import Trade
from .utils import utc_now

class Broker:
    pass

class BacktestBroker(Broker):
    def __init__(self, hub: Hub) -> None:
        self.hub = hub
        self.publisher = Publisher(hub, prefix='broker')
        self.subscriber = Subscriber(hub, 'broker')
        self.subscriber.add_sync_listener(events.AnyNewTrade,
                                          self.log_trade_timestamp)
        self.orders = []
        self.positions = []
        self._timestamp = None

    def submit_order(self, order: Order) -> None:
        order.timestamp = self.get_timestamp()
        exchange = order.exchange
        self.publisher.publish([exchange.name, 'new-order'], order)
        self.orders.append(order)
        position = self.make_position(order)
        self.positions.append(position)
        position.open(order.price)

    def make_position(self, order: Order) -> Position:
        position = Position(order.market.quote,
                            order.amount,
                            timestamp=order.timestamp)
        self.publisher.publish([str(order.market), 'new-position'], position)
        return position

    def get_timestamp(self) -> datetime:
        if self._timestamp is not None:
            return self._timestamp
        else:
            return utc_now()

    def log_trade_timestamp(self, key: Key, trade: Trade) -> None:
        self._timestamp = trade.timestamp


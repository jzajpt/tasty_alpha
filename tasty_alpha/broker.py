from aiopubsub import Hub, Publisher
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from .exchange import Exchange
from .market import Market
from .position import Position
from .order import Order, OrderType, OrderSide

class Broker:
    pass

class BacktestBroker(Broker):
    def __init__(self, hub: Hub) -> None:
        self.hub = hub
        self.publisher = Publisher(hub, prefix='broker')
        self.orders = []
        self.positions = []

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
        return datetime.now()



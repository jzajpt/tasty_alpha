from aiopubsub import Key, Hub, Subscriber
import numpy as np
from .market import Market
from .position import Position

class PositionManager:
    """
    PositionManager handles opening, closing and book-keeping of positions
    on the market.
    """

    def __init__(self, hub: Hub, market: Market):
        self.subscriber = Subscriber(hub, 'PositionManager')
        new_position = Key('*', '*', 'new-position')
        self.subscriber.add_sync_listener(new_position, self.on_new_position)
        self.market = market
        self.position = None
        self.positions = []
        self.closed_positions = []

    @property
    def is_open(self) -> bool:
        """
        Is any position open?
        """
        return bool(self.position)

    def on_new_position(self, key: Key, position: Position) -> None:
        self.positions.append(position)
        self.position = position

    def close_position(self, price: float) -> None:
        if not self.position:
            raise Exception("Cannot close position when no position open!")
        self.position.close(price)
        self.closed_positions.append(self.position)
        self.position = None

    def total_realized_pnl(self) -> float:
        """
        Returns realized PnL of all past (closed) positions.
        """
        return np.sum([pos.realized_pnl for pos in self.closed_positions])


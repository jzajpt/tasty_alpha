import numpy as np
from .asset import Asset
from .position import Position

class PositionManager:
    """
    PositionManager handles opening, closing and book-keeping of positions
    """

    def __init__(self, asset: Asset):
        self.asset = asset
        self.position = None
        self.past_positions = []

    @property
    def is_open(self) -> bool:
        """
        Is any position open?
        """
        return bool(self.position)

    def open_position(self, amount: float, price: float) -> None:
        if self.position:
            raise Exception("Cannot open position if one is already open!")
        self.position = Position(self.asset, amount)
        self.position.open(price)

    def close_position(self, price: float) -> None:
        if not self.position:
            raise Exception("Cannot close position when no position open!")
        self.position.close(price)
        self.past_positions.append(self.position)
        self.position = None

    def total_realized_pnl(self) -> float:
        """
        Returns realized PnL of all past (closed) positions.
        """
        return np.sum([pos.realized_pnl for pos in self.past_positions])

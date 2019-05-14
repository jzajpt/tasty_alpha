from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field
from .asset import Asset

class PositionStatus(Enum):
    """
    Wrapper class for different statuses position can be in.
    """

    Pending = "Pending"
    Open = "Open"
    Closing = "Closing"
    Closed = "Closed"

@dataclass
class Position:
    """
    Tracks a position in an asset.

    Attributes:
    - asset (Asset) - an asset position is help in
    - amount (float) - an amount or quantity of an asset
    - status (PositionStatus) - a status of an position
    - cost (float) - total cost to acquire position
    - realized_pnl (float) - total realized pnl after closing position incl fees
    """
    asset: Asset
    amount: float
    status: str = PositionStatus.Pending
    cost: float = None
    timestamp: datetime = field(default_factory=datetime.now)
    realized_pnl: float = None
    unrealized_pnl: float = None

    def open(self, price: float, fees: float = 0.0) -> None:
        self.cost = (price * self.amount) + fees
        self.status = PositionStatus.Open

    def close(self, price: float, fees: float = 0.0) -> None:
        self.income = (price * self.amount) - fees
        self.realized_pnl = self.income - self.cost
        self.status = PositionStatus.Closed


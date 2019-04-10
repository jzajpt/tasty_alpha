from .asset import Asset

class PositionStatus:
    """
    Wrapper class for different statuses position can be in.
    """

    Pending = "Pending"
    Open = "Open"
    Closing = "Closing"
    Closed = "Closed"

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

    def __init__(self, asset: Asset, amount: float) -> None:
        self.asset = asset
        self.amount = amount
        self.status = PositionStatus.Pending
        self.cost = None
        self.realized_pnl = None
        self.unrealized_pnl = None

    def open(self, price: float, fees: float = 0.0) -> None:
        self.cost = (price * self.amount) + fees
        self.status = PositionStatus.Open

    def close(self, price: float, fees: float = 0.0) -> None:
        self.income = (price * self.amount) - fees
        self.realized_pnl = self.income - self.cost
        self.status = PositionStatus.Closed


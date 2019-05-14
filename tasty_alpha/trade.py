from dataclasses import dataclass

@dataclass
class Trade:
    """
    Represents a trade that has occured on a market.

    Attributes:
    timestamp (int)
    amount (float)
    price (float)
    """
    timestamp: int
    amount: float
    price: float

    @property
    def dollar_value(self) -> float:
        return self.price * self.amount


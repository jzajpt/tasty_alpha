class Trade:
    def __init__(self, timestamp: int, amount: float, price: float) -> None:
        self.timestamp = timestamp
        self.amount = amount
        self.price = price

    @property
    def dollar_value(self) -> float:
        return self.price * self.amount


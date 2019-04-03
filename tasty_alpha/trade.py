class Trade:
    def __init__(self, timestamp, amount, price):
        self.timestamp = timestamp
        self.amount = amount
        self.price = price

    @property
    def dollar_value(self):
        return self.price * self.amount


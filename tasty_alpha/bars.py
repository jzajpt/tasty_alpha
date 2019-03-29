from blinker import signal

class Bar:
    def __init__(self, first_trade):
        self.open = first_trade.price
        self.high = first_trade.price
        self.low = first_trade.price
        self.close = first_trade.price
        self.total_value = first_trade.price * first_trade.amount
        self.count = 1
        self.new_trade = signal('new-trade')
        self.new_trade.connect(self.on_new_trade)
        self.threshold_reached = signal('threshold-reached')
        self.threshold_reached.connect(self.on_threshold_reached)

    def __repr__(self):
        return f"[{self.open}, {self.high}, {self.low}, {self.close}] {self.count}"

    def on_threshold_reached(self, bar):
        print(self)
        self.new_trade.disconnect(self.on_new_trade)
        self.threshold_reached.disconnect(self.on_threshold_reached)

    def on_new_trade(self, trade):
        if self.count == 0:
            self.open = trade.price
        if not self.high or trade.price > self.high:
            self.high = trade.price
        if not self.low or trade.price < self.low:
            self.low = trade.price
        self.close = trade.price
        self.total_value = trade.price * trade.amount
        self.count += 1


class ThresholdBars:
    def __init__(self, threshold):
        self.new_trade = signal('new-trade')
        self.new_trade.connect(self.on_new_trade)
        self.threshold_reached = signal('threshold-reached')
        self.threshold = threshold
        self.bar = None
        self.value = 0

    def on_new_trade(self, trade):
        if not self.bar:
            self.bar = Bar(trade)
        if self.value > self.threshold:
            self.value = 0
            self.threshold_reached.send()
            self.bar = Bar(trade)
        self.value += self.metric(trade)

class TickBars(ThresholdBars):
    def metric(self, trade):
        return 1

class VolumeBars(ThresholdBars):
    def metric(self, trade):
        return trade.amount

class DollarBars(ThresholdBars):
    def metric(self, trade):
        return trade.amount * trade.price


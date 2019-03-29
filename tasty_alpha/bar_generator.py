import datetime
from functools import partial
from blinker import signal
import pandas as pd

COLUMN_NAMES = ['time', 'price', 'amount']

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
        return f"{self.open}-{self.high}-{self.low}-{self.close}-{self.count}"

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


class CSVTradeProcessor:
    def __init__(self, filename):
        self.filename = filename
        self.df = pd.read_csv(self.filename, names=COLUMN_NAMES)
        self.df.time = pd.to_datetime(self.df.time, unit='s')
        self.new_trade = signal('new-trade')

    def run(self):
        self.df.apply(self.send_signal, axis=1)

    def send_signal(self, trade):
        signal('new-trade').send(trade)

class ThresholdBars:
    def __init__(self):
        self.new_trade = signal('new-trade')
        self.new_trade.connect(self.on_new_trade)
        self.threshold_reached = signal('threshold-reached')
        self.bar = None

    def on_new_trade(self, trade):
        pass

class TickBars:
    def __init__(self, threshold = 100):
        self.new_trade = signal('new-trade')
        self.new_trade.connect(self.on_new_trade)
        self.threshold_reached = signal('threshold-reached')
        self.threshold = threshold
        self.count = 0
        self.bar = None

    def on_new_trade(self, trade):
        if not self.bar:
            self.bar = Bar(trade)
        self.count += 1
        if self.count > self.threshold:
            self.count = 0
            self.threshold_reached.send()
            self.bar = Bar(trade)


class DollarBars:
    def __init__(self, threshold = 25000):
        self.new_trade = signal('new-trade')
        self.new_trade.connect(self.on_new_trade)
        self.threshold_reached = signal('threshold-reached')
        self.threshold = threshold
        self.cumsum = 0
        self.bar = None

    def on_new_trade(self, trade):
        if not self.bar:
            self.bar = Bar(trade)
        value = trade.price * trade.amount
        self.cumsum += value
        if self.cumsum > self.threshold:
            self.cumsum = 0
            self.threshold_reached.send()
            self.bar = Bar(trade)


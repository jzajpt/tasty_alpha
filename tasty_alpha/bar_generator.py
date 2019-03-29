import datetime
from blinker import signal
import pandas as pd

COLUMN_NAMES = ['time', 'price', 'amount']

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


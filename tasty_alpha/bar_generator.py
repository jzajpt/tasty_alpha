import datetime
from blinker import signal
import pandas as pd

COLUMN_NAMES = ['time', 'price', 'amount']
new_bar = signal('new-bar')
processing_finished = signal('processing-finished')

class CSVTradeProcessor:
    def __init__(self, filename):
        self.filename = filename
        self.df = pd.read_csv(self.filename, names=COLUMN_NAMES)
        self.df.time = pd.to_datetime(self.df.time, unit='s')

    def run(self):
        self.df.apply(self.send_signal, axis=1)
        processing_finished.send()

    def send_signal(self, trade):
        signal('new-trade').send(trade)

class CSVBarWriter:
    def __init__(self, filename):
        self.filename = filename
        new_bar.connect(self.on_new_bar)
        processing_finished.connect(self.on_processing_finished)
        self.bars = []

    def on_new_bar(self, bar):
        print(bar)
        self.bars.append(bar.to_dict())

    def on_processing_finished(self, sender):
        df = pd.DataFrame(self.bars)
        print(df.head())
        df.to_csv(self.filename)



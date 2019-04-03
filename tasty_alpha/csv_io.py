import asyncio
from aiopubsub import Publisher, Subscriber, Key
import datetime
import pandas as pd
from .trade import Trade

COLUMN_NAMES = ['time', 'price', 'amount']

class CSVTradeProcessor:
    def __init__(self, hub, filename):
        self.filename = filename
        print("Reading csv")
        self.df = pd.read_csv(self.filename, names=COLUMN_NAMES)
        self.df.time = pd.to_datetime(self.df.time, unit='s')
        self.publisher = Publisher(hub, prefix='csv_trade_processor')
        print("Reading done")

    async def run(self):
        print("Processing")
        self.df.apply(self.send_signal, axis=1)
        self.publisher.publish('processing-finished', '')

    def send_signal(self, row):
        trade = Trade(timestamp=row.time, price=row.price, amount=row.amount)
        self.publisher.publish('new-trade', trade)


class CSVBarWriter:
    def __init__(self, hub, filename):
        self.filename = filename
        self.subscriber = Subscriber(hub, 'csv_bar_writer')
        new_bar_key = Key('*', 'new-bar')
        self.subscriber.add_sync_listener(new_bar_key, self.on_new_bar)
        self.subscriber.add_sync_listener('processing-finished',
                self.on_processing_finished)
        self.bars = []

    def on_new_bar(self, key, bar):
        print(bar)
        self.bars.append(bar.to_dict())

    def on_processing_finished(self, key, message):
        df = pd.DataFrame(self.bars)
        print(df.head())
        df.to_csv(self.filename)



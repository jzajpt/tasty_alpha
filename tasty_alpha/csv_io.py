import asyncio
from aiopubsub import Hub, Publisher, Subscriber, Key
import datetime
from loguru import logger
import pandas as pd
from .bar import Bar
from .trade import Trade

COLUMN_NAMES = ['time', 'price', 'amount']

# TODO: Rewrite this as generator
# for trade in CSVTradeProcessor:
class CSVTradeProcessor:
    def __init__(self, hub: Hub, filename: str) -> None:
        self.filename = filename
        logger.info("Reading csv")
        self.df = pd.read_csv(self.filename, names=COLUMN_NAMES)
        self.df.time = pd.to_datetime(self.df.time, unit='s')
        self.publisher = Publisher(hub, prefix='csv_trade_processor')
        logger.info("Reading done")

    def run(self) -> None:
        logger.info("Processing trades from CSV")
        self.df.apply(self.send_signal, axis=1)
        logger.info("Finished, sending signal")
        self.publisher.publish(Key('processing-finished'), None)

    def send_signal(self, row) -> None:
        trade = Trade(timestamp=row.time, price=row.price, amount=row.amount)
        self.publisher.publish('new-trade', trade)


class CSVBarWriter:
    def __init__(self, hub: Hub, filename: str) -> None:
        self.filename = filename
        self.subscriber = Subscriber(hub, 'csv_bar_writer')
        new_bar_key = Key('*', 'new-bar')
        self.subscriber.add_sync_listener(new_bar_key, self.on_new_bar)
        processing_finished_key = Key('*', 'processing-finished')
        self.subscriber.add_sync_listener(processing_finished_key,
                self.on_processing_finished)
        self.bars = []

    def on_new_bar(self, key: Key, bar: Bar) -> None:
        logger.info('CSVBarWriter#on_new_bar {bar}', bar=bar)
        self.bars.append(bar.to_dict())

    def on_processing_finished(self, key: Key, _: None) -> None:
        logger.info('Saving CSV file with bars')
        df = pd.DataFrame(self.bars)
        print(df.head())
        df.to_csv(self.filename)


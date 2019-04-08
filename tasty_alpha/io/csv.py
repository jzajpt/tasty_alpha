import asyncio
from aiopubsub import Hub, Publisher, Subscriber, Key
import datetime
from loguru import logger
import pandas as pd
from ..sampling.bar import Bar
from ..trade import Trade
from .. import events

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
        self.publisher.publish(events.ProcessingFinished, None)

    def send_signal(self, row) -> None:
        trade = Trade(timestamp=row.time, price=row.price, amount=row.amount)
        self.publisher.publish('new-trade', trade)


class CSVBarWriter:
    def __init__(self, hub: Hub, filename: str, dump_wait: bool = True) -> None:
        self.filename = filename
        self.subscriber = Subscriber(hub, 'csv_bar_writer')
        self.subscriber.add_sync_listener(events.AnyNewBar, self.on_new_bar)
        self.subscriber.add_sync_listener(events.AnyProcessingFinished,
                self.on_processing_finished)
        self.bars = []
        self.dump_wait = dump_wait

    def on_new_bar(self, key: Key, bar: Bar) -> None:
        self.bars.append(bar.to_dict())
        if not self.dump_wait:
            self.on_processing_finished(None, None)

    def on_processing_finished(self, key: Key, _: None) -> None:
        logger.info('Saving CSV file with bars')
        df = pd.DataFrame(self.bars)
        logger.info(df.head())
        df.to_csv(self.filename)



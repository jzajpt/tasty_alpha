from aiopubsub import Hub, Publisher
import pandas as pd
from arctic import Arctic
from arctic.date import DateRange
from loguru import logger
from .csv import COLUMN_NAMES
from ..trade import Trade
from .. import events

def ingest_trades(filename: str, library: str, symbol: str) -> None:
    store = Arctic('localhost')
    # Defaults to VersionStore
    store.initialize_library(library)
    library = store[library]

    df = pd.read_csv(filename, names=COLUMN_NAMES)
    df.time = pd.to_datetime(df.time, unit='s')

    library.write(symbol, df, metadata={'source': 'bitcoincharts'})

class ArcticTradeProcessor:
    def __init__(self, hub: Hub, library: str, symbol: str) -> None:
        self.symbol = symbol
        self.store = Arctic('localhost')
        self.library = self.store[library]
        self.publisher = Publisher(hub, prefix='csv_trade_processor')

    def run(self) -> None:
        logger.info("Processing trades from Arctic")
        date_range = DateRange('2016-01-01', '2019-01-01')
        item = self.library.read(self.symbol, date_range=date_range)
        df = item.data
        df.apply(self.send_signal, axis=1)
        logger.info("Finished, sending signal")
        self.publisher.publish(events.ProcessingFinished, None)

    def send_signal(self, row) -> None:
        trade = Trade(timestamp=row.time, price=row.price, amount=row.amount)
        self.publisher.publish('new-trade', trade)


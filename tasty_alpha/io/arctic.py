from aiopubsub import Hub, Publisher
import pandas as pd
from arctic import Arctic
from arctic.date import DateRange
from loguru import logger
from typing import Optional
from .csv import COLUMN_NAMES
from ..exchange import Exchange
from ..trade import Trade
from ..market import Market
from .. import events

def ingest_trades(filename: str, library: str, symbol: str) -> None:
    store = Arctic('localhost')
    logger.info(f"Saving to library: {library}, symbol: {symbol}")
    # Defaults to VersionStore
    store.initialize_library(library)
    library = store[library]
    df = pd.read_csv(filename, names=COLUMN_NAMES)
    df.time = pd.to_datetime(df.time, unit='s')
    library.write(symbol, df, metadata={'source': 'csv'})

class ArcticTradeProcessor:
    def __init__(self, hub: Hub,
                 exchange: Exchange,
                 market: Market,
                 date_range: Optional[DateRange] = None
                 ) -> None:
        self.library_name = str(exchange)
        self.symbol = str(market)
        self.store = Arctic('localhost')
        self.library = self.store[self.library_name]
        self.date_range = date_range
        self.publisher = Publisher(hub, prefix='arctic_trade_processor')

    def run(self) -> None:
        logger.info("Processing trades from Arctic")
        item = self.library.read(self.symbol, date_range=self.date_range)
        logger.info("Finished reading, launching trades")
        item.data.apply(self.send_signal, axis=1)
        self.publisher.publish(events.ProcessingFinished, None)

    def send_signal(self, row) -> None:
        trade = Trade(timestamp=row.time, price=row.price, amount=row.amount)
        self.publisher.publish([f"{self.library_name}-{self.symbol}", 'new-trade'], trade)


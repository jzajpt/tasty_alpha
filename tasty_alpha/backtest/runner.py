import asyncio
import aiopubsub
from typing import Union, TextIO, Optional
from ..io.csv import CSVTradeProcessor, CSVBarWriter
from ..io.arctic import ArcticTradeProcessor
from ..market import Market, Markets
from ..strategy import MovingAverageCrossStrategy
from ..sampling.bar_generators import DollarBarGenerator, TickBarGenerator, \
    VolumeBarGenerator, PossibleBarTypes, new_bar_generator

async def run_backtest(bar: str,
                       threshold: int) -> None:
    hub = aiopubsub.Hub()
    bar_generator = new_bar_generator(bar, hub, threshold)
    bar_writer = CSVBarWriter(hub, 'output.csv')
    exchange = 'kraken'
    market = Markets.BTCUSD
    strategy = MovingAverageCrossStrategy(hub, exchange, market)
    trade_processor = ArcticTradeProcessor(hub, exchange, market)
    trade_processor.run()
    asyncio.get_event_loop().stop()



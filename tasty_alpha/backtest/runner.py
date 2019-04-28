import aiopubsub
import asyncio
from arctic.date import DateRange
from typing import Union, TextIO, Optional
from ..io.csv import CSVTradeProcessor, CSVBarWriter
from ..io.arctic import ArcticTradeProcessor
from ..exchange import Exchange, Exchanges
from ..market import Market, Markets
from ..strategy import Strategy, read_and_run_strategy_file
from ..sampling.bar import Bar
from ..sampling.bar_generators import DollarBarGenerator, TickBarGenerator, \
    VolumeBarGenerator, PossibleBarTypes, new_bar_generator

async def run_backtest(file: str,
                       start,
                       end,
                       bar: str,
                       threshold: int) -> None:
    hub = aiopubsub.Hub()
    bar_generator = new_bar_generator(bar, hub, threshold)
    bar_writer = CSVBarWriter(hub, 'output.csv')
    strategy = read_and_run_strategy_file(file)(hub)
    if start is not None:
        date_range = DateRange(start, end)
    else:
        date_range = None
    trade_processor = ArcticTradeProcessor(hub,
                                          strategy.exchange,
                                          strategy.market,
                                          date_range)
    trade_processor.run()
    asyncio.get_event_loop().stop()



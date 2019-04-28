import aiopubsub
import asyncio
from arctic.date import DateRange
import re
import runpy
from typing import Union, TextIO, Optional
from ..io.csv import CSVTradeProcessor, CSVBarWriter
from ..io.arctic import ArcticTradeProcessor
from ..exchange import Exchange, Exchanges
from ..market import Market, Markets
from ..strategy import Strategy
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
    strategy_file = None
    strategy_name = None
    with open(file, 'r') as f:
        strategy_file = f.read()
        strategy_name = re.search("class (.+)\(Strategy\):", strategy_file)[1]

    strategy_code = runpy.run_path(file)
    strategy = strategy_code[strategy_name](hub)
    if start is not None:
        date_range = DateRange(start, end)
    else:
        date_range = None
    trade_processor = ArcticTradeProcessor(hub, strategy.exchange,
            strategy.market, date_range)
    trade_processor.run()
    asyncio.get_event_loop().stop()



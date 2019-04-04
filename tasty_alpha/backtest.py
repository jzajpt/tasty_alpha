import asyncio
import aiopubsub
from typing import Union
from .csv_io import CSVTradeProcessor, CSVBarWriter
from .bar_generators import DollarBarGenerator, TickBarGenerator, \
    VolumeBarGenerator, PossibleBarTypes, new_bar_generator

async def run_backtest(file: str, bar: str, threshold: int) -> None:
    hub = aiopubsub.Hub()
    bar_generator = new_bar_generator(bar, hub, threshold)
    bar_writer = CSVBarWriter(hub, 'output.csv')
    trade_processor = CSVTradeProcessor(hub, file)
    trade_processor.run()
    asyncio.get_event_loop().stop()


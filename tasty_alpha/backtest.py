import asyncio
import aiopubsub
from typing import Union
from .csv_io import CSVTradeProcessor, CSVBarWriter
from .bar_generators import DollarBarGenerator, TickBarGenerator, \
    VolumeBarGenerator, PossibleBarTypes

def new_bar_generator(bar: str,
        hub: aiopubsub.Hub,
        threshold: int
        ) -> PossibleBarTypes:
    if bar == 'tick':
        return TickBarGenerator(hub, threshold)
    elif bar == 'dollar':
        return  DollarBarGenerator(hub, threshold)
    elif bar == 'volume':
        return  VolumeBarGenerator(hub, threshold)
    else:
        raise Exception(f'Invalid bar generator type: {bar}')

async def run_backtest(file: str, bar: str, threshold: int) -> None:
    hub = aiopubsub.Hub()
    bar_generator = new_bar_generator(bar, hub, threshold)
    bar_writer = CSVBarWriter(hub, 'output.csv')
    trade_processor = CSVTradeProcessor(hub, file)
    trade_processor.run()
    asyncio.get_event_loop().stop()


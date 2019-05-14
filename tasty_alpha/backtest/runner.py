import aiopubsub
import asyncio
from arctic.date import DateRange
from loguru import logger
from typing import Union, TextIO, Optional
from ..io.csv import CSVTradeProcessor, CSVBarWriter
from ..io.arctic import ArcticTradeProcessor
from ..broker import BacktestBroker
from ..exchange import Exchange, Exchanges
from ..market import Market, Markets
from ..strategy import Strategy, read_and_run_strategy_file
from ..sampling.bar import Bar
from ..sampling.bar_generators import new_bar_generator

async def run_backtest(file: str,
                       start,
                       end,
                       capital: float,
                       bar: str,
                       threshold: int) -> None:
    hub = aiopubsub.Hub()
    bar_generator = new_bar_generator(bar, hub, threshold)
    bar_writer = CSVBarWriter(hub, 'output.csv')
    p1s = [5, 11, 17, 20]
    p2s = [40, 60, 80]
    for p1, p2 in zip(p1s, p2s):
        logger.info("{p1} {p2} starting", p1=p1, p2=p2)
        broker = BacktestBroker(hub)
        strategy = read_and_run_strategy_file(file)(hub, broker, p1=p1, p2=p2)
        if start is not None:
            print(start)
            print(end)
            date_range = DateRange(start, end)
        else:
            date_range = None
        trade_processor = ArcticTradeProcessor(hub,
                                               strategy.exchange,
                                               strategy.market,
                                               date_range)
        trade_processor.run()
        logger.info(f"total realized pnl: {strategy.position_manager.total_realized_pnl()}")
    asyncio.get_event_loop().stop()



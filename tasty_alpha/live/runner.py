from aiopubsub import Hub
from cryptofeed import exchanges
from ..sampling.bar_generators import new_bar_generator
from ..io.csv import CSVBarWriter
from ..io.feed import FeedProcessor
from ..strategy import read_and_run_strategy_file


def run_livefeed(file: str,
                bar_type: str,
                threshold: int,
                exchange_name: str,
                pair: str) -> None:
    hub = Hub()
    bar_generator = new_bar_generator(bar_type, hub, threshold)
    filename = 'output-live.csv'
    bar_writer = CSVBarWriter(hub, filename, dump_wait=False)
    strategy = read_and_run_strategy_file(file)(hub)
    exchange = getattr(exchanges, exchange_name)
    trade_processor = FeedProcessor(hub, exchange, pair)
    trade_processor.run()


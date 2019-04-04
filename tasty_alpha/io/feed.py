from aiopubsub import Hub, Key, Publisher, Subscriber
from cryptofeed.callback import TradeCallback
from cryptofeed import FeedHandler
from cryptofeed.exchanges import Bitmex, Coinbase, Bitfinex, Poloniex, Gemini, HitBTC, Bitstamp, Kraken, Binance
from cryptofeed.defines import TRADES
from loguru import logger
from ..sampling.bar import Bar
from ..sampling.bar_generators import new_bar_generator
from ..io.csv import CSVBarWriter
from ..trade import Trade

class FeedProcessor:
    def __init__(self, hub: Hub, pair: str) -> None:
        self.feed = FeedHandler()
        self.publisher = Publisher(hub, prefix='feed_processor')
        binance_feed = Binance(pairs=[pair],
                channels=[TRADES],
                callbacks={TRADES: TradeCallback(self.trade)})
        self.feed.add_feed(binance_feed)

    def run(self) -> None:
        self.feed.run()

    async def trade(self, feed, pair, order_id, timestamp, side, amount, price):
        # print(f"Timestamp: {timestamp} Feed: {feed} Pair: {pair} ID: {order_id} Side: {side} Amount: {amount} Price: {price}")
        trade = Trade(timestamp=timestamp, price=price, amount=amount)
        self.publisher.publish('new-trade', trade)

def run_livefeed(bar_type: str, threshold: int, pair: str) -> None:
    hub = Hub()
    bar_generator = new_bar_generator(bar_type, hub, threshold)
    filename = 'output-live.csv'
    bar_writer = CSVBarWriter(hub, filename, dump_wait=False)
    trade_processor = FeedProcessor(hub, pair)
    trade_processor.run()


from aiopubsub import Hub, Publisher, Subscriber
from cryptofeed.callback import TradeCallback
from cryptofeed import FeedHandler
from cryptofeed.exchanges import Bitmex, Coinbase, Bitfinex, Poloniex, Bitstamp, Kraken, Binance
from cryptofeed.defines import TRADES
from cryptofeed.feed import Feed
from loguru import logger
from ..sampling.bar import Bar
from ..trade import Trade

class FeedProcessor:
    def __init__(self, hub: Hub, exchange_class: str, pair: str) -> None:
        self.feed = FeedHandler()
        self.publisher = Publisher(hub, prefix='feed_processor')
        self.pair = pair
        self._add_feed(exchange_class)

    def _add_feed(self, exchange_class: str):
        trades_feed = exchange_class(pairs=[self.pair],
                                     channels=[TRADES],
                                     callbacks={TRADES: TradeCallback(self.trade)})
        self.feed.add_feed(trades_feed)

    def run(self) -> None:
        self.feed.run()

    async def trade(self, feed, pair, order_id, timestamp, side, amount, price):
        # print(f"Timestamp: {timestamp} Feed: {feed} Pair: {pair} ID: {order_id} Side: {side} Amount: {amount} Price: {price}")
        trade = Trade(timestamp=timestamp, price=price, amount=amount)
        self.publisher.publish([self.pair, 'new-trade'], trade)


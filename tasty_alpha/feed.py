from cryptofeed.callback import TickerCallback, TradeCallback, BookCallback, FundingCallback
from cryptofeed import FeedHandler
from cryptofeed.exchanges import Bitmex, Coinbase, Bitfinex, Poloniex, Gemini, HitBTC, Bitstamp, Kraken, Binance, EXX, Huobi
from cryptofeed.defines import L3_BOOK, L2_BOOK, BID, ASK, TRADES, TICKER, FUNDING, COINBASE
from blinker import signal
from .trade import Trade

class FeedProcessor:
    def __init__(self):
        self.feed = FeedHandler()
        binance_feed = Binance(pairs=['BTC-USDT'],
                channels=[TRADES],
                callbacks={TRADES: TradeCallback(self.trade)})
        self.feed.add_feed(binance_feed)

    def run(self):
        self.feed.run()

    async def trade(self, feed, pair, order_id, timestamp, side, amount, price):
        print(f"Timestamp: {timestamp} Feed: {feed} Pair: {pair} ID: {order_id} Side: {side} Amount: {amount} Price: {price}")
        trade = Trade(timestamp=timestamp, price=price, amount=amount)
        signal('new-trade').send(trade)


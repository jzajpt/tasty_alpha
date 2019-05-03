class Exchange:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name.lower()


class Exchanges:
    Binance = Exchange('Binance')
    Bitstamp = Exchange('Bitstamp')
    Bitfinex = Exchange('Bitfinex')
    Coinbase = Exchange('Coinbase')
    Kraken = Exchange('Kraken')
    Poloniex = Exchange('Poloniex')


from dataclasses import dataclass

@dataclass
class Exchange:
    name: str

    def __str__(self):
        return self.name.lower()

    @staticmethod
    def default():
        return Exchanges.Bitstamp


class Exchanges:
    Binance = Exchange('Binance')
    Bitstamp = Exchange('Bitstamp')
    Bitfinex = Exchange('Bitfinex')
    Coinbase = Exchange('Coinbase')
    Kraken = Exchange('Kraken')
    Poloniex = Exchange('Poloniex')


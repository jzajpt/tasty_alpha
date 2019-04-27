class Exchange:
    def __init__(self, name):
        self.name = name

class Exchanges:
    Bitstamp = Exchange('Bitstamp')
    Coinbase = Exchange('Coinbase')
    Kraken = Exchange('Kraken')


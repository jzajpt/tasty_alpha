class Exchange:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name.lower()


class Exchanges:
    Bitstamp = Exchange('Bitstamp')
    Coinbase = Exchange('Coinbase')
    Kraken = Exchange('Kraken')


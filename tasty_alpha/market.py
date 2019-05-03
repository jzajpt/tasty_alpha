from .asset import Asset, Assets

class Market:
    def __init__(self, base: Asset, quote: Asset):
        self.quote = quote
        self.base = base

    def __str__(self):
        return f"{self.base.ticker}{self.quote.ticker}"

class Markets:
    BTCUSD = Market(Assets.BTC, Assets.USD)
    BTCEUR = Market(Assets.BTC, Assets.EUR)
    LTCBTC = Market(Assets.LTC, Assets.BTC)


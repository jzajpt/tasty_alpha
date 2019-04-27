from .asset import Asset, Assets

class Market:
    def __init__(self, quote: Asset, base: Asset):
        self.quote = quote
        self.base = base

    def __str__(self):
        return f"{self.quote.ticker}{self.base.ticker}"

class Markets:
    BTCUSD = Market(Assets.BTC, Assets.USD)
    BTCEUR = Market(Assets.BTC, Assets.EUR)
    LTCBTC = Market(Assets.LTC, Assets.BTC)


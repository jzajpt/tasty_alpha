from dataclasses import dataclass
from .asset import Asset, Assets

@dataclass
class Market:
    base: Asset
    quote: Asset

    def __str__(self):
        return f"{self.base.ticker}{self.quote.ticker}"

class Markets:
    BTCUSD = Market(Assets.BTC, Assets.USD)
    BTCEUR = Market(Assets.BTC, Assets.EUR)
    LTCBTC = Market(Assets.LTC, Assets.BTC)


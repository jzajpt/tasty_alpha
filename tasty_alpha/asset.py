class Asset:
    """
    Represents an asset - future, index, crypto, etc.

    Attributes:
    - ticker - short letter code representing ticker
    - name - long name of the asset
    """
    def __init__(self, ticker: str, name: str = None) -> None:
        self.ticker = ticker
        self.name = name

class Assets:
    BTC = Asset("BTC", "Bitcoin")


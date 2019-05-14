from dataclasses import dataclass

@dataclass
class Asset:
    """
    Represents an asset - future, index, crypto, etc.

    Attributes:
    - ticker - short letter code representing ticker
    - name - long name of the asset
    """
    ticker: str
    name: str = None

class Assets:
    BTC = Asset("BTC", "Bitcoin")
    LTC = Asset("LTC", "Litecoin")
    XRP = Asset("XRP", "Ripple")
    USDT = Asset("USDT", "US Dollar Tether")

    EUR = Asset("EUR", "Euro")
    USD = Asset("USD", "US Dollar")
    GBP = Asset("GBP", "British Pound")


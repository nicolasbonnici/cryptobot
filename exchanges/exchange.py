from strategies.strategy import Strategy


class Exchange:
    currency: str
    asset: str
    strategy: Strategy

    def __init__(self, key: str, secret: str):
        self.apiKey = key
        self.apiSecret = secret
        self.name = None
        self.client = None
        self.socketManager = None
        self.socket = None
        self.currency = ''
        self.asset = ''
        self.strategy = None

    def get_symbol(self):
        return self.currency + "_" + self.asset

    def set_currency(self, symbol: str):
        self.currency = symbol

    def set_asset(self, symbol: str):
        self.asset = symbol

    def set_strategy(self, strategy: Strategy):
        self.strategy = strategy

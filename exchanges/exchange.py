from models import price


class Exchange:
    currency: str
    asset: str

    def __init__(self, key: str, secret: str):
        self.apiKey = key
        self.apiSecret = secret
        self.name = None
        self.client = None
        self.socketManager = None
        self.socket = None
        self.currency = None
        self.asset = None
        self.strategy = None

    def get_symbol(self):
        return self.currency + "_" + self.asset

    def set_currency(self, symbol: str):
        self.currency = symbol

    def set_asset(self, symbol: str):
        self.asset = symbol

    def set_strategy(self, strategy):
        self.strategy = strategy

    def process(self, msg):
        if msg['e'] == 'error':
            print(msg)
            self.close_socket()
        else:
            self.strategy.run(
                price.Price(pair=self.get_symbol(), currency=self.currency, asset=self.asset,  exchange=self.name, current=msg['b'], lowest=msg['l'], highest=msg['h'])
            )
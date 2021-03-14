from datetime import datetime

from api import utils
from exchanges.exchange import Exchange
from strategies.strategy import Strategy


class Runner(Strategy):
    def __init__(self, exchange: Exchange, timeout=60, *args, **kwargs):
        super().__init__(exchange, timeout, *args, **kwargs)
        self.buy_price = 0
        self.sell_price = 0
        self.stop_loss = 0

        self.market_delta = 0

        self.advised = False
        self.waiting_order = False
        self.fulfilled_orders = []
        self.last_price = 0

    def run(self):
        print('*******************************')
        print('Exchange: ', self.exchange.name)
        print('Pair: ', self.exchange.get_symbol())
        print('Available: ', self.exchange.get_asset_balance(self.exchange.currency) + ' ' + self.exchange.currency)
        print('Available: ', self.exchange.get_asset_balance(self.exchange.currency) + ' ' + self.exchange.asset)
        print('Price: ', self.price.current)

        # Persist price
        response = self.price.create()
        print(response)
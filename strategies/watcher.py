from decouple import config
from models.price import Price
from models.order import Order
from datetime import datetime
from strategies.strategy import Strategy


class Watcher(Strategy):
    def __init__(self, exchange, timeout=60, *args, **kwargs):
        super().__init__(exchange, timeout)

    def run(self):
        response = self.exchange.symbol_ticker()
        price = Price(pair=self.exchange.get_symbol(), currency=self.exchange.currency, asset=self.exchange.asset,  exchange=self.exchange.name, current=response['price'])

        # print(self.exchange.get_asset_balance(self.exchange.currency))

        print('*******************************')
        print('Exchange: ', price.exchange)
        print('Pair: ', price.pair)
        print('Price: ', price.current)

        self.buy(quantity=100, price=price.current)

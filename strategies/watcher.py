from decouple import config
from models.price import Price
from datetime import datetime
from strategies.strategy import Strategy


class Watcher(Strategy):
    def __init__(self, exchange, timeout=60, *args, **kwargs):
        super().__init__(exchange, timeout)

    def run(self):
        response = self.exchange.symbol_ticker()
        newPrice = Price(pair=self.exchange.get_symbol(), currency=self.exchange.currency, asset=self.exchange.asset,  exchange=self.exchange.name, current=response['price'])

        print('*******************************')
        print('Exchange: ', newPrice.exchange)
        print('Pair: ', newPrice.pair)
        print('Price: ', newPrice.current)

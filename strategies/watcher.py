from decouple import config
from models import price
from datetime import datetime
from strategies.strategy import Strategy


class Watcher(Strategy):
    def __init__(self, exchange, timeout=60, *args, **kwargs):
        super().__init__(exchange, timeout)

    def run(newPrice: price.Price):
        print('*******************************')
        print('Exchange: ', newPrice.exchange)
        print('Pair: ', newPrice.pair)
        print('Price: ', newPrice.current)

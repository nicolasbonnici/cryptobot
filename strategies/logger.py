from exchanges.exchange import Exchange
from strategies.strategy import Strategy


class Logger(Strategy):
    def __init__(self, exchange: Exchange, timeout=60, *args, **kwargs):
        super().__init__(exchange, timeout, *args, **kwargs)

    def run(self):
        self.get_price()
        print('*******************************')
        print('Exchange: ', self.exchange.name)
        print('Pair: ', self.exchange.get_symbol())
        print('Price: ', self.price.current)

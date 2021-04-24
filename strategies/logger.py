from exchanges.exchange import Exchange
from strategies.strategy import Strategy
from models.pair import Pair


class Logger(Strategy):
    def __init__(self, exchange: Exchange, pair: Pair, timeout=60, *args, **kwargs):
        super().__init__(exchange, pair, timeout, *args, **kwargs)

    def run(self):
        print('*******************************')
        print('Exchange: ', self.exchange.name)
        print('Pair: ', self.exchange.get_symbol(self.pair))
        print('Price: ', self.price.current)

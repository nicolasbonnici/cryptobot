from exchanges.exchange import Exchange
from strategies.strategy import Strategy


class Watcher(Strategy):
    def __init__(self, exchange: Exchange, timeout=60, *args, **kwargs):
        super().__init__(exchange, timeout, *args, **kwargs)

    def run(self):
        print('*******************************')
        print('Exchange: ', self.exchange.name)
        print('Pair: ', self.exchange.get_symbol())
        print('Available: ', self.portfolio['currency'] + ' ' + self.exchange.currency)
        print('Available: ', self.portfolio['asset'] + ' ' + self.exchange.asset)
        print('Price: ', self.price.current)

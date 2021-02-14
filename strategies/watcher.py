from exchanges.exchange import Exchange
from strategies.strategy import Strategy


class Watcher(Strategy):
    def __init__(self, exchange: Exchange, timeout=60, *args, **kwargs):
        super().__init__(exchange, timeout, *args, **kwargs)
        self.portfolio = {'currency': self.exchange.get_asset_balance(self.exchange.currency),
                          'asset': self.exchange.get_asset_balance(self.exchange.asset)}

    def run(self):
        price = self.exchange.symbol_ticker()

        print('*******************************')
        print('Exchange: ', price.exchange)
        print('Currency available: ', self.portfolio['currency'] + ' ' + self.exchange.currency)
        print('Asset available: ', self.portfolio['asset'] + ' ' + self.exchange.asset)
        print('Pair: ', price.pair)
        print('Price: ', price.current)

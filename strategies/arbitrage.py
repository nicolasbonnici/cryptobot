from strategies.strategy import Strategy


class Arbitrage(Strategy):
    def __init__(self, exchange, timeout=60, *args, **kwargs):
        super().__init__(exchange, timeout, *args, **kwargs)
        self.exchanges = ['binance', 'bitfinex', 'kraken']
        self.currencies = ['bitcoin', 'ethereum', 'monero']
        self.asset = ['EUR']

    def run(self):
        for coin in self.currencies:
            response = self.exchange.get_client().symbol_ticker()
            print(response)

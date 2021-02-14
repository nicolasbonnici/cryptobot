from exchanges import exchange


class Coinbase(exchange.Exchange):
    def __init__(self, key: str, secret: str):
        exchange.Exchange.__init__(self, key, secret)
        # self.client = CoinbaseAccount(self.apiKey, self.apiSecret)
        self.name = self.__class__.__name__

    def get_client(self):
        return self.client

    def get_symbol(self):
        return self.currency + '_to_' + self.asset

    def symbol_ticker(self):
        response = self.client.exchange_rates([self.get_symbol()])
        self.process(response)

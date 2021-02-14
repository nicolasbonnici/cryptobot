from decouple import config
from strategies.strategy import Strategy
from models import price
from pycoingecko import CoinGeckoAPI
from twisted.internet import task, reactor
from exchanges.coin_gecko import CoinGecko

class Arbitrage(Strategy):
    def __init__(self, exchange, timeout=60, *args, **kwargs):
        super().__init__(exchange, timeout)
        self.exchanges = ['binance','bitfinex','kraken']
        self.currencies = ['bitcoin','ethereum','monero']
        self.asset = ['EUR']

    def run(self):
            coin_data = []
            for coin in self.currencies:
                response = self.exchange.get_client().symbol_ticker()
                print(response)

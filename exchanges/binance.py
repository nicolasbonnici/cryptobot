from exchanges import exchange
from models.price import Price
from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor

class Binance(exchange.Exchange):
    def __init__(self, key: str, secret: str):
        exchange.Exchange.__init__(self, key, secret)
        self.client = Client(self.apiKey, self.apiSecret)
        self.name = self.__class__.__name__

    def get_client(self):
        return self.client

    def get_binance_symbol(self):
        return self.currency + self.asset

    def get_socket_manager(self):
        return BinanceSocketManager(self.client)

    def symbol_ticker_candle(self, interval=Client.KLINE_INTERVAL_1MINUTE):
        response: object = self.client.get_klines(symbol=self.get_binance_symbol(),  interval=interval)
        print(response)

    def historical_symbol_ticker_candle(self, start: str, end=None, interval=Client.KLINE_INTERVAL_1MINUTE):
        for candle in self.client.get_historical_klines_generator(self.get_binance_symbol(), interval, start, end):
            print(candle)

    def symbol_ticker(self):
        response = self.client.get_symbol_ticker(self.symbol)
        self.process(response)

    def start_symbol_ticker_socket(self, symbol: str):
        self.socketManager = self.get_socket_manager()
        self.socket = self.socketManager.start_symbol_ticker_socket(symbol=self.get_binance_symbol(), callback=self.process)

        self.start_socket()

    def start_socket(self):
        print('Start WebSocket connection...')
        self.socketManager.start()

    def close_socket(self):
        self.socketManager.stop_socket(self.socket)
        self.socketManager.close()
        # properly terminate WebSocket
        reactor.stop()

    def process(self, msg):
        if msg['e'] == 'error':
            print(msg)
            self.close_socket()
        else:
            self.strategy.run(
                Price(pair=self.get_symbol(), currency=self.currency, asset=self.asset,  exchange=self.name, current=msg['b'], lowest=msg['l'], highest=msg['h'])
            )
from exchanges import exchange
from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor


class Binance(exchange.Exchange):
    def __init__(self, key: str, secret: str):
        exchange.Exchange.__init__(self, key, secret)
        self.client = Client(self.apiKey, self.apiSecret)

    def get_client(self):
        return self.client

    def get_socket_manager(self):
        return BinanceSocketManager(self.client)

    def start_symbol_ticker_socket(self, symbol: str):
        self.socketManager = self.get_socket_manager()
        self.socket = self.socketManager.start_symbol_ticker_socket(symbol, self.process)

        self.start_socket()

    def start_socket(self):
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
            self.strategy.run(msg)
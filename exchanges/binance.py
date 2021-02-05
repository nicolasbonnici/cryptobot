from exchanges import exchange
from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor
from strategies import debug


class Binance(exchange.Exchange):
    def __init__(self, key: str, secret: str):
        exchange.Exchange.__init__(self, key, secret)
        self.client = Client(self.apiKey, self.apiSecret)
        self.socketManager = None
        self.socket = None

    def get_client(self):
        return self.client

    def start_symbol_ticker_socket(self, symbol: str):
        self.socketManager = BinanceSocketManager(self.client)
        # start symbol ticker socket
        self.socket = self.socketManager.start_symbol_ticker_socket(symbol, self.process)

        # then start the socket manager
        self.socketManager.start()

    def process(self, msg):
        if msg['e'] == 'error':
            print(msg)
            self.close_socket()
        else:
            debug.run(msg)

    def close_socket(self):
        self.socketManager.stop_socket(self.socket)
        self.socketManager.close()
        # properly terminate WebSocket
        reactor.stop()

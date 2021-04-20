import datetime
from api import utils
from abc import ABC, abstractmethod
from twisted.internet import reactor
from strategies.strategy import Strategy
from models.order import Order
from models.currency import Currency
from models.pair import Pair


class Exchange(ABC):
    strategy: Strategy

    def __init__(self, key: str, secret: str):
        self.apiKey = key
        self.apiSecret = secret
        self.name = None
        self.client = None
        self.socketManager = None
        self.socket = None
        self.strategy = None

    def set_strategy(self, strategy: Strategy):
        self.strategy = strategy

    # abstract methods

    # Override to set current exchange symbol pair notation (default with _ separator currency_asset ex: eur_btc)
    @abstractmethod
    def get_symbol(self, pair: Pair):
        return utils.format_pair(pair.currency, pair.asset)

    # Get current symbol ticker
    @abstractmethod
    def symbol_ticker(self):
        pass

    # Get current symbol ticker candle for given interval
    @abstractmethod
    def symbol_ticker_candle(self, interval):
        pass

    # Get current symbol historic value
    @abstractmethod
    def historical_symbol_ticker_candle(self, pair: Pair, start: datetime, end=None, interval=60):
        pass

    # Get balance for a given currency
    @abstractmethod
    def get_asset_balance(self, currency: Currency):
        pass

    # Create an exchange order
    @abstractmethod
    def order(self, order: Order):
        pass

    # Create an exchange test order
    @abstractmethod
    def test_order(self, order: Order):
        pass

    # Check an exchange order status
    @abstractmethod
    def check_order(self, orderId):
        pass

    # Cancel an exchange order
    @abstractmethod
    def cancel_order(self, orderId):
        pass

    # WebSocket related methods

    @abstractmethod
    def get_socket_manager(self, purchase):
        pass

    @abstractmethod
    def websocket_event_handler(self, msg):
        pass

    def start_socket(self):
        print('Starting WebSocket connection...')
        self.socketManager.start()

    def close_socket(self):
        self.socketManager.stop_socket(self.socket)
        self.socketManager.close()
        # properly terminate WebSocket
        reactor.stop()

    @abstractmethod
    def start_symbol_ticker_socket(self, pair: Pair):
        pass

import datetime
from api import utils
from abc import ABC, abstractmethod
from twisted.internet import reactor
from strategies.strategy import Strategy
from models.order import Order


class Exchange(ABC):
    currency: str
    asset: str
    strategy: Strategy

    def __init__(self, key: str, secret: str):
        self.apiKey = key
        self.apiSecret = secret
        self.name = None
        self.client = None
        self.socketManager = None
        self.socket = None
        self.currency = ''
        self.asset = ''
        self.strategy = None

    def set_currency(self, symbol: str):
        self.currency = symbol

    def set_asset(self, symbol: str):
        self.asset = symbol

    def set_strategy(self, strategy: Strategy):
        self.strategy = strategy

    def compute_symbol_pair(self):
        return utils.format_pair(self.currency, self.asset)

    # abstract methods

    # Override to set current exchange symbol pair notation (default with _ separator currency_asset ex: eur_btc)
    @abstractmethod
    def get_symbol(self):
        return self.compute_symbol_pair(self)

    # Override if current exchange support WebSocket connection
    @abstractmethod
    def start_symbol_ticker_socket(self, symbol: str):
        pass

    # Override if current exchange support WebSocket connection
    @abstractmethod
    def get_socket_manager(self, purchase):
        pass

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
    def historical_symbol_ticker_candle(self, start: datetime, end=None, interval=60):
        pass

    # Get balance for a given currency
    @abstractmethod
    def get_asset_balance(self, currency):
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
    def websocket_event_handler(self, msg):
        pass

    @abstractmethod
    def start_symbol_ticker_socket(self, symbol: str):
        pass

    def start_socket(self):
        print('Starting WebSocket connection...')
        self.socketManager.start()

    def close_socket(self):
        self.socketManager.stop_socket(self.socket)
        self.socketManager.close()
        # properly terminate WebSocket
        reactor.stop()
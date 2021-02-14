from binance.client import Client
from binance.enums import *
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor

from exchanges import exchange
from models.order import Order
from models.price import Price


class Binance(exchange.Exchange):
    def __init__(self, key: str, secret: str):
        super().__init__(key, secret)

        self.client = Client(self.apiKey, self.apiSecret)
        self.name = self.__class__.__name__

    def get_client(self):
        return self.client

    def get_symbol(self):
        return self.currency + self.asset

    def get_socket_manager(self):
        return BinanceSocketManager(self.client)

    def symbol_ticker_candle(self, interval=Client.KLINE_INTERVAL_1MINUTE):
        return self.client.get_klines(symbol=self.get_symbol(), interval=interval)

    def historical_symbol_ticker_candle(self, start: str, end=None, interval=Client.KLINE_INTERVAL_1MINUTE):
        for candle in self.client.get_historical_klines_generator(self.get_symbol(), interval, start, end):
            print(candle)

    def symbol_ticker(self):
        response = self.client.get_symbol_ticker(symbol=self.get_symbol())
        return Price(pair=self.get_symbol(), currency=self.currency, asset=self.asset, exchange=self.name,
                     current=response['price'])

    def start_symbol_ticker_socket(self, symbol: str):
        self.socketManager = self.get_socket_manager()
        self.socket = self.socketManager.start_symbol_ticker_socket(symbol=self.get_symbol(), callback=self.process)

        self.start_socket()

    def get_account(self):
        return self.client.get_account()

    def get_asset_balance(self, currency):
        response = self.client.get_asset_balance(currency)
        return response['free']

    def order(self, order: Order):
        return self.client.create_order(
            symbol=order.symbol,
            side=order.side,
            type=order.type,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=order.quantity,
            price=order.price
        )

    def test_order(self, order: Order):
        return self.client.create_test_order(
            symbol=order.symbol,
            side=order.side,
            type=order.type,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=order.quantity,
            price=order.price
        )

    def check_order(self, orderId):
        return client.get_order(
            symbol=self.get_symbol(),
            orderId=orderId
        )

    def cancel_order(self, orderId):
        return client.cancel_order(
            symbol=self.get_symbol(),
            orderId=orderId
        )

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
                Price(pair=self.get_symbol(), currency=self.currency, asset=self.asset, exchange=self.name,
                      current=msg['b'], lowest=msg['l'], highest=msg['h'])
            )

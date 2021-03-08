import datetime
from math import floor

from binance.client import Client
from binance.enums import *
from binance.websockets import BinanceSocketManager

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

    def symbol_ticker(self):
        response = self.client.get_symbol_ticker(symbol=self.get_symbol())
        return Price(pair=self.get_symbol(), currency=self.currency.lower(), asset=self.asset.lower(), exchange=self.name.lower(),
                     current=response['price'])

    def symbol_ticker_candle(self, interval=Client.KLINE_INTERVAL_1MINUTE):
        return self.client.get_klines(symbol=self.get_symbol(), interval=interval)

    def historical_symbol_ticker_candle(self, start: datetime, end=None, interval=Client.KLINE_INTERVAL_1MINUTE):
        if isinstance(interval, int):
            interval = str(floor(interval/60)) + 'm'
        print(interval)
        for candle in self.client.get_historical_klines_generator(self.get_symbol(), interval, start.strftime('%Y-%m-%dT%H:%M:%SZ'), end):
            print(candle)

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
        return self.client.get_order(
            symbol=self.get_symbol(),
            orderId=orderId
        )

    def cancel_order(self, orderId):
        return self.client.cancel_order(
            symbol=self.get_symbol(),
            orderId=orderId
        )

    def websocket_event_handler(self, msg):
        if msg['e'] == 'error':
            print(msg)
            self.close_socket()
        else:
            self.strategy.run(
                Price(pair=self.get_symbol(), currency=self.currency, asset=self.asset, exchange=self.name,
                      current=msg['b'], lowest=msg['l'], highest=msg['h'])
            )

from datetime import datetime
from math import floor

from binance.client import Client
from binance.enums import *
from binance.websockets import BinanceSocketManager

from api import utils
from exchanges import exchange
from models.order import Order
from models.price import Price
from models.pair import Pair


class Binance(exchange.Exchange):
    def __init__(self, key: str, secret: str):
        super().__init__(key, secret)

        self.client = Client(self.apiKey, self.apiSecret)
        self.name = self.__class__.__name__

    def get_client(self):
        return self.client

    @staticmethod
    def get_symbol(pair: Pair):
        return pair.currency + pair.asset

    def symbol_ticker(self, pair: Pair):
        symbol = self.get_symbol(pair)
        response = self.client.get_symbol_ticker(symbol=symbol)
        print(response)
        return Price(pair=symbol, currency=pair.currency.lower(), asset=pair.asset.lower(), exchange=self.name.lower(),
                     current=response['price'], openAt=utils.format_date(datetime.now()))

    def symbol_ticker_candle(self, pair: Pair, interval=Client.KLINE_INTERVAL_1MINUTE):
        return self.client.get_klines(symbol=self.get_symbol(pair), interval=interval)

    def historical_symbol_ticker_candle(self, pair: Pair, start: datetime, end=None,
                                        interval=Client.KLINE_INTERVAL_1MINUTE):
        # Convert default seconds interval to string like "1m"
        if isinstance(interval, int):
            interval = str(floor(interval/60)) + 'm'

        output = []
        for candle in self.client.get_historical_klines_generator(self.get_symbol(pair), interval, start, end):
            """
                [
                    [
                        1499040000000,      # Open time
                        "0.01634790",       # Open
                        "0.80000000",       # High
                        "0.01575800",       # Low
                        "0.01577100",       # Close
                        "148976.11427815",  # Volume
                        1499644799999,      # Close time
                        "2434.19055334",    # Quote asset volume
                        308,                # Number of trades
                        "1756.87402397",    # Taker buy base asset volume
                        "28.46694368",      # Taker buy quote asset volume
                        "17928899.62484339" # Can be ignored
                    ]
                ]

            """
            output.append(
                Price(pair=self.get_symbol(pair), currency=pair.currency.lower(), asset=pair.asset.lower(),
                      exchange=self.name.lower(),
                      current=float(candle[1]), lowest=float(candle[3]), highest=float(candle[2]),
                      volume=float(candle[5]), openAt=utils.format_date(datetime.fromtimestamp(int(candle[0]) / 1000)))
            )

        return output

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

    def check_order(self, pair: Pair, orderId):
        return self.client.get_order(
            symbol=self.get_symbol(pair),
            orderId=orderId
        )

    def cancel_order(self, pair: Pair, orderId):
        return self.client.cancel_order(
            symbol=self.get_symbol(pair),
            orderId=orderId
        )

    def get_socket_manager(self):
        return BinanceSocketManager(self.client)

    def start_symbol_ticker_socket(self, pair: Pair):
        self.socketManager = self.get_socket_manager()
        self.socket = self.socketManager.start_symbol_ticker_socket(
            symbol=self.get_symbol(pair),
            callback=self.websocket_event_handler
        )

        self.start_socket()

    def websocket_event_handler(self, pair: Pair, msg):
        if msg['e'] == 'error':
            print(msg)
            self.close_socket()
        else:
            self.strategy.set_price(
                Price(pair=self.get_symbol(pair), currency=pair.currency, asset=pair.asset, exchange=self.name,
                      current=msg['b'], lowest=msg['l'], highest=msg['h'])
            )
            self.strategy.run()

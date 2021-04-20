import threading
import time
from datetime import datetime
from abc import ABC, abstractmethod
from decouple import config

from models.order import Order
from models.price import Price
from models.pair import Pair


class Strategy(ABC):
    TRADING_MODE_TEST = 'test'
    TRADING_MODE_REAL = 'real'

    price: Price

    def __init__(self, exchange, pair: Pair, interval=60, *args, **kwargs):
        self.exchange = exchange
        self._timer = None
        self.interval = interval
        self.pair = pair
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time.time()
        self.portfolio = {}
        self.test = bool(config('TRADING_MODE') != self.TRADING_MODE_REAL)

    def _run(self):
        self.is_running = False
        self.start()
        self.set_price(self.exchange.symbol_ticker(self.pair))
        self.run()

    @abstractmethod
    def run(self):
        pass

    def start(self):
        if not self.is_running:
            print(datetime.now())
            if self._timer is None:
                self.next_call = time.time()
            else:
                self.next_call += self.interval

            self._timer = threading.Timer(self.next_call - time.time(), self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

    def get_portfolio(self):
        self.portfolio = {'currency': self.exchange.get_asset_balance(self.pair.currency),
                          'asset': self.exchange.get_asset_balance(self.pair.asset)}

    def get_price(self):
        return self.price

    def set_price(self, price: Price):
        self.price = price

    def buy(self, **kwargs):
        order = Order(
            currency=self.pair.currency,
            asset=self.pair.asset,
            symbol=self.exchange.get_symbol(self.pair),
            type=Order.TYPE_LIMIT,
            side=Order.BUY,
            test=self.test,
            **kwargs
        )
        self.order(order)

    def sell(self, **kwargs):
        order = Order(
            currency=self.pair.currency,
            asset=self.pair.asset,
            symbol=self.exchange.get_symbol(self.pair),
            side=Order.SELL,
            test=self.test,
            **kwargs
        )
        self.order(order)

    def order(self, order: Order):
        print(order)
        if self.test:
            exchange_order = self.exchange.test_order(order)
        else:
            exchange_order = self.exchange.order(order)

        print(exchange_order)

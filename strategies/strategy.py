import json
import threading
import time
from datetime import datetime

import requests
from decouple import config

from models.order import Order
from models.price import Price


class Strategy(object):
    TRADING_MODE_TEST = 'test'
    TRADING_MODE_REAL = 'real'

    price: Price

    def __init__(self, exchange, interval=60, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time.time()
        self.portfolio = {}
        self.test = bool(config('DEFAULT_TRADING_MODE') != self.TRADING_MODE_REAL)
        self.exchange = exchange
        # Load account portfolio for pair at load
        self.get_portfolio()

    def _run(self):
        self.get_price()
        self.persist_price()
        self.is_running = False
        self.start()
        self.run(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            print(datetime.now())
            self.next_call += self.interval
            self._timer = threading.Timer(self.next_call - time.time(), self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

    def get_portfolio(self):
        self.portfolio = {'currency': self.exchange.get_asset_balance(self.exchange.currency),
                          'asset': self.exchange.get_asset_balance(self.exchange.asset)}

    def get_price(self):
        self.price = self.exchange.symbol_ticker()

    # Persist price on internal API
    def persist_price(self):
        url = config('API_ENDPOINT_PRICE')
        data = self.price.__dict__
        data['currency'] = '/api/currencies/' + data['currency']
        data['asset'] = '/api/currencies/' + data['asset']
        data['exchange'] = '/api/exchanges/' + data['exchange']
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        request = requests.post(url, data=json.dumps(data), headers=headers)
        return request.json()

    def buy(self, **kwargs):
        order = Order(
            currency=self.exchange.currency,
            asset=self.exchange.asset,
            symbol=self.exchange.get_symbol(),
            type=Order.TYPE_LIMIT,
            side=Order.BUY,
            test=self.test,
            **kwargs
        )
        self.order(order)

    def sell(self, **kwargs):
        order = Order(
            currency=self.exchange.currency,
            asset=self.exchange.asset,
            symbol=self.exchange.get_symbol(),
            side=Order.SELL,
            test=self.test,
            **kwargs
        )
        self.order(order)

    def order(self, order: Order):
        print(order)
        if self.test:
            exchangeOrder = self.exchange.test_order(order)
        else:
            exchangeOrder = self.exchange.order(order)

        print(exchangeOrder)

    def datetime_normalizer(o, i):
        if isinstance(o, datetime):
            return o.isoformat()
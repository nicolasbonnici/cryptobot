from datetime import datetime

from api import utils
from api.rest import Rest
from exchanges.exchange import Exchange
from strategies.strategy import Strategy


class Runner(Strategy):
    def __init__(self, exchange: Exchange, timeout=60, *args, **kwargs):
        super().__init__(exchange, timeout, *args, **kwargs)
        self.rest = Rest()
        self.buy_price = 0
        self.sell_price = 0
        self.stop_loss = 0

        self.market_delta = 0

        self.advised = False
        self.waiting_order = False
        self.fulfilled_orders = []
        self.last_price = 0

    def run(self):
        print('*******************************')
        print('Exchange: ', self.exchange.name)
        print('Pair: ', self.exchange.get_symbol())
        print('Available: ', self.portfolio['currency'] + ' ' + self.exchange.currency)
        print('Available: ', self.portfolio['asset'] + ' ' + self.exchange.asset)
        print('Price: ', self.price.current)

        # Persist price
        data = self.price.__dict__
        data['currency'] = '/api/currencies/' + data['currency']
        data['asset'] = '/api/currencies/' + data['asset']
        data['exchange'] = '/api/exchanges/' + data['exchange']
        data['openAt'] = utils.format_date(datetime.now())
        data['dataset'] = '/api/datasets/f06db3d5-1d29-4f2d-9b41-a785a9b429b1'
        response = self.rest.post('prices', data=data)
        print(response.json())
import sys
from datetime import datetime
from decouple import config
from models.price import Price
from api.rest import Rest

class Importer:
    def __init__(self, exchange, periodStart: datetime, periodEnd=None, interval=60, *args, **kwargs):
        self.exchange = exchange
        self.interval = interval
        self.periodStart = periodStart
        self.periodEnd = periodEnd
        self.start = datetime.now()
        self.rest = Rest()

    def process(self):
        for price in self.exchange.historical_symbol_ticker_candle(self.periodStart, self.periodEnd, self.interval):
            print(self.persist(price).json())

        executionTime = datetime.now() - self.start
        print('Execution time: ' + str(executionTime.total_seconds()) + ' seconds')
        sys.exit()

    # Persist price on internal API
    def persist(self, price: Price):
        try:
            data = price.__dict__
            data['currency'] = '/api/currencies/' + data['currency']
            data['asset'] = '/api/currencies/' + data['asset']
            data['exchange'] = '/api/exchanges/' + data['exchange']
            data['dataset'] = '/api/datasets/f06db3d5-1d29-4f2d-9b41-a785a9b429b1'
            response = self.rest.post('prices', data=data)
            return response
        except Exception as e:
            pass

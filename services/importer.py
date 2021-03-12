import sys
from datetime import datetime
from models.dataset import Dataset


class Importer:
    def __init__(self, exchange, period_start: datetime, period_end=None, interval=60, *args, **kwargs):
        self.exchange = exchange
        self.interval = interval
        self.periodStart = period_start
        self.periodEnd = period_end
        self.start = datetime.now()
        self.dataset = Dataset()
        self.dataset.persist(
            {'exchange': self.exchange.name, 'periodStart': period_start, 'periodEnd': period_end,
             'currency': self.exchange.currency, 'asset': self.exchange.asset})

    def process(self):
        for price in self.exchange.historical_symbol_ticker_candle(self.periodStart, self.periodEnd, self.interval):
            print(price.persist({'dataset': self.dataset.uuid}))

        execution_time = datetime.now() - self.start
        print('Execution time: ' + str(execution_time.total_seconds()) + ' seconds')
        sys.exit()

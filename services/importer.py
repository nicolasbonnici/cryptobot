import sys
from datetime import datetime
from models.dataset import Dataset
from models.pair import Pair


class Importer:
    def __init__(self, exchange, pair: Pair, period_start: datetime, period_end=None, interval=60, *args, **kwargs):
        self.exchange = exchange
        self.interval = interval
        self.period_start = period_start
        self.period_end = period_end
        self.start = datetime.now()
        self.dataset = Dataset().create(
            data={'exchange': self.exchange.name, 'periodStart': self.period_start, 'periodEnd': self.period_end,
                  'candleSize': 60,
                  'currency': pair.currency, 'asset': pair.asset})

    def process(self):
        for price in self.exchange.historical_symbol_ticker_candle(self.period_start, self.period_end, self.interval):
            print(price.create({'dataset': self.dataset.uuid}))

        execution_time = datetime.now() - self.start
        print('Execution time: ' + str(execution_time.total_seconds()) + ' seconds')
        sys.exit()

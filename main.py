#!/usr/bin/python3

import importlib
import signal
import sys
import threading
from decouple import config

from models.dataset import Dataset
from models.price import Price
from services.importer import Importer

exchange_name = config('EXCHANGE')
available_exchanges = config('AVAILABLE_EXCHANGES').split(',')
mode: str = config('MODE')
strategy: str = config('STRATEGY')
trading_mode: str = config('TRADING_MODE')
interval: int = int(config('CANDLE_INTERVAL'))
currency: str = config('CURRENCY')
asset: str = config('ASSET')

if trading_mode == 'real':
    print("*** Caution: Trading mode activated ***")
else:
    print("Test mode")

# Parse symbol pair from first command argument
if len(sys.argv) > 1:
    currencies = sys.argv[1].split('_')
    if len(currencies) > 1:
        currency = currencies[0]
        asset = currencies[1]

# Load exchange
print("Connecting to {} exchange...".format(exchange_name[0].upper() + exchange_name[1:]))
exchangeModule = importlib.import_module('exchanges.' + exchange_name, package=None)
exchangeClass = getattr(exchangeModule, exchange_name[0].upper() + exchange_name[1:])
exchange = exchangeClass(config(exchange_name.upper() + '_API_KEY'), config(exchange_name.upper() + '_API_SECRET'))

# Load currencies
exchange.set_currency(currency)
exchange.set_asset(asset)

# Load strategy
strategyModule = importlib.import_module('strategies.' + strategy, package=None)
strategyClass = getattr(strategyModule, strategy[0].upper() + strategy[1:])
exchange.set_strategy(strategyClass(exchange, interval))

# mode
print("{} mode on {} symbol".format(mode, exchange.get_symbol()))
if mode == 'trade':
    exchange.strategy.start()

elif mode == 'live':
    exchange.start_symbol_ticker_socket(exchange.get_symbol())

elif mode == 'backtest':
    period_start = config('PERIOD_START')
    period_end = config('PERIOD_END')

    print(
        "Backtest period from {} to {} with {} seconds candlesticks.".format(
            period_start,
            period_end,
            interval
        )
    )

    # Try to find dataset
    dataset = Dataset().query('get', {"exchange": '/api/exchanges/'+exchange.name.lower(), "currency": '/api/currency/'+currency.lower(), "asset": '/api/currency/'+asset.lower(),
                              "period_start": period_start, "period_end": period_end, "candleSize": interval})

    if dataset and len(dataset) > 0:
        print(dataset[0])
        price = Price()
        for price in price.query('get', {"dataset": dataset[0]['uuid']}):
            newPrice = Price()
            newPrice.populate(price)
            exchange.strategy.set_price(newPrice)
            exchange.strategy.run()
    else:
        print("Dataset not found, external API call to " + exchange.name)
        for price in exchange.historical_symbol_ticker_candle(period_start, period_end, interval):
            exchange.strategy.set_price(price)
            exchange.strategy.run()

    sys.exit()

elif mode == 'import':
    period_start = config('PERIOD_START')
    period_end = config('PERIOD_END')

    print(
        "Import mode on {} symbol for period from {} to {} with {} seconds candlesticks.".format(
            exchange.get_symbol(),
            period_start,
            period_end,
            interval
        )
    )
    importer = Importer(exchange, period_start, period_end, interval)
    importer.process()

else:
    print('Not supported mode.')


def signal_handler(signal, frame):
    if (exchange.socket):
        print('Closing WebSocket connection...')
        exchange.close_socket()
        sys.exit(0)
    else:
        print('stopping strategy...')
        exchange.strategy.stop()
        sys.exit(0)


# Listen for keyboard interrupt event
signal.signal(signal.SIGINT, signal_handler)
forever = threading.Event()
forever.wait()
exchange.strategy.stop()
sys.exit(0)

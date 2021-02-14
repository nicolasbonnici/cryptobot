#!/usr/bin/python3
from decouple import config
import signal
import sys
import threading
from exchanges import binance, coinbase, exchange
from strategies import debug, watcher, arbitrage

exchange_name = config('DEFAULT_EXCHANGE')
available_exchanges = config('AVAILABLE_EXCHANGES').split(',')
mode: str = config('DEFAULT_MODE')
strategy: str = config('DEFAULT_STRATEGY')
trading_mode: str = config('DEFAULT_TRADING_MODE')
interval: int = int(config('DEFAULT_TRADE_CANDLESTICK_INTERVAL'))
currency: str = config('DEFAULT_CURRENCY')
asset: str = config('DEFAULT_ASSET')

# Parse symbol pair from first  command argument
if len(sys.argv) > 1:
    symbol = sys.argv[1]
    currencies = sys.argv[1].split('_')
    if len(currencies) > 1:
        currency = currencies[0]
        asset = currencies[1]

if trading_mode == 'real':
    print("*** Caution: Trading mode activated ***")
else:
    print("Test mode")

print("Connecting to {} exchange...".format(exchange_name[0].upper() + exchange_name[1:]))
if exchange_name == 'binance':
    exchange = binance.Binance(config('BINANCE_API_KEY'), config('BINANCE_API_SECRET'))
if exchange_name == 'coinbase':
    exchange = coinbase.Coinbase(config('COINBASE_API_KEY'), config('COINBASE_API_SECRET'))
if exchange_name == 'coin_gekko':
    exchange = coinbase.Coinbase(config('COINGE_API_KEY'), config('COINBASE_API_SECRET'))

exchange.set_currency(currency)
exchange.set_asset(asset)

# Load strategy TODO DRY with factory
if strategy == 'debug':
    exchange.set_strategy(debug.Debug(exchange, interval))

if strategy == 'watcher':
    exchange.set_strategy(watcher.Watcher(exchange, interval))

if strategy == 'arbitrage':
    exchange.set_strategy(arbitrage.Arbitrage(exchange, interval))

# Start mode
print("{} mode on {} symbol".format(mode, exchange.get_symbol()))
if mode == 'trader':
    exchange.strategy.start()

elif mode == 'live':
    exchange.start_symbol_ticker_socket(exchange.get_symbol())

elif mode == 'backtest':
    period_start = config('DEFAULT_PERIOD_START')
    period_end = config('DEFAULT_PERIOD_END')

    print("Backtest mode on {} symbol for period from {} to {} with {} candlesticks.".format(symbol, period_start,
                                                                                             period_end, interval))
    exchange.historical_symbol_ticker_candle(period_start, period_end, interval)

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

# Listen for keyboard interrupt event to close socket
signal.signal(signal.SIGINT, signal_handler)
forever = threading.Event()
forever.wait()


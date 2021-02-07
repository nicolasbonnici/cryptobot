#!/usr/bin/python3
from decouple import config
import signal
import sys
import threading
from exchanges import binance
from strategies import debug, watcher

exchange_name = config('EXCHANGE')
mode: str = config('DEFAULT_MODE')
strategy: str = config('DEFAULT_STRATEGY')
trading_mode: str = config('DEFAULT_TRADING_MODE')
interval: str = config('DEFAULT_TRADE_CANDLESTICK_INTERVAL')
symbol: str = config('DEFAULT_SYMBOL')

print("Connecting to {} exchange...".format(exchange_name[0].upper() + exchange_name[1:]))
exchange = binance.Binance(config('BINANCE_API_KEY'), config('BINANCE_API_SECRET'))

# Parse symbol pair from first  command argument
if len(sys.argv) > 1:
    symbol = sys.argv[1]

exchange.set_symbol(symbol)

if strategy == 'debug':
    exchange.set_strategy(debug)


def signal_handler(signal, frame):
    print('Closing WebSocket connection...')
    exchange.close_socket()
    sys.exit(0)


if trading_mode == 'real':
    print("*** Caution: Trading mode activated ***")
else:
    print("Test mode")

if mode == 'watcher' or mode == 'live':
    print("{} mode on {} symbol".format(mode, symbol))

    if mode == 'watcher':
        exchange.set_strategy(watcher)

    exchange.start_symbol_ticker_socket(symbol)

    # Listen for keyboard interrupt event to close socket
    signal.signal(signal.SIGINT, signal_handler)
    forever = threading.Event()
    forever.wait()

if mode == 'backtest':
    period_start = config('DEFAULT_PERIOD_START')
    period_end = config('DEFAULT_PERIOD_END')

    print("Backtest mode on {} symbol for period from {} to {} with {} candlesticks.".format(symbol, period_start,
                                                                                             period_end, interval))
    exchange.historical_symbol_ticker_candle(period_start, period_end, interval)

#!/usr/bin/python3
from decouple import config
import signal
import sys
import threading
from exchanges import binance
from strategies import debug

exchange_name = config('EXCHANGE')
symbol = config('DEFAULT_SYMBOL')

print("Connecting to {} exchange...".format(exchange_name[0].upper() + exchange_name[1:]))
exchange = binance.Binance(config('BINANCE_API_KEY'), config('BINANCE_API_SECRET'))
exchange.set_strategy(debug)


def signal_handler(signal, frame):
    print('Closing WebSocket connection...')
    exchange.close_socket()
    sys.exit(0)


if len(sys.argv) > 1:
    symbol = sys.argv[1]

print("Watch price for {} symbol.".format(symbol))
exchange.start_symbol_ticker_socket(symbol)

# Listen for keyboard interrupt event to close socket
signal.signal(signal.SIGINT, signal_handler)
forever = threading.Event()
forever.wait()

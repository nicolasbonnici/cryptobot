#!/usr/bin/python3
from decouple import config
import signal
import sys
import threading
from exchanges import binance

symbol = config('DEFAULT_SYMBOL')

exchange = binance.Binance(config('BINANCE_API_KEY'), config('BINANCE_API_SECRET'))
client = exchange.get_client()


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

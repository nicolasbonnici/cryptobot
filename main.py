#!/usr/bin/python3
from decouple import config
import signal
import sys
import threading
from twisted.internet import reactor
from binance.client import Client
from binance.websockets import BinanceSocketManager
from strategies.margin import strat

symbol = config('DEFAULT_SYMBOL')
client = Client(config('BINANCE_API_KEY'), config('BINANCE_API_SECRET'))


def process(msg):
    if msg['e'] == 'error':
        print(msg)
        close_socket()
    else:
        strat(msg)


def signal_handler(signal, frame):
    print('Closing WebSocket connection...')
    close_socket()
    sys.exit(0)


def close_socket():
    bm.stop_socket(conn_key)
    bm.close()
    # properly terminate WebSocket
    reactor.stop()


if len(sys.argv) > 1:
    symbol = sys.argv[1]

print("Watch price for {} symbol.".format(symbol))
bm = BinanceSocketManager(client)
# start symbol ticker socket
conn_key = bm.start_symbol_ticker_socket(symbol, process)

# then start the socket manager
bm.start()

# Listen for keyboard interrupt event
signal.signal(signal.SIGINT, signal_handler)
forever = threading.Event()
forever.wait()

from datetime import datetime
from time import sleep

from strategy import Strategy


class Debug(Strategy):
    def __init__(self, exchange, timeout=60, *args, **kwargs):
        super().__init__(exchange, timeout, *args, **kwargs)

    def run(self):
        print(datetime.now().time())
        sleep(10)

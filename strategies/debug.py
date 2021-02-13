from datetime import datetime
from .strategy import Strategy
from time import sleep


class Debug(Strategy):
    def __init__(self, exchange, timeout=60, *args, **kwargs):
        super().__init__(exchange, timeout)

    def run(self):
        print(datetime.now().time())
        sleep(10)

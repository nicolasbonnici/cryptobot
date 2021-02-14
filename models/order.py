from decouple import config
import uuid
import datetime

class Order():
    BUY = 'BUY'
    SELL = 'SELL'

    TYPE_LIMIT = 'LIMIT'
    TYPE_MARKET = 'MARKET'
    TYPE_STOP_LOSS = 'STOP_LOSS'
    TYPE_STOP_LOSS_LIMIT = 'STOP_LOSS_LIMIT'
    TYPE_TAKE_PROFIT = 'TAKE_PROFIT'
    TYPE_TAKE_PROFIT_LIMIT = 'TAKE_PROFIT_LIMIT'
    TYPE_LIMIT_MAKER = 'LIMIT_MAKER'
    
    def __init__(self, **kwargs):
        self.uuid = ''
        self.side = ''
        self.type = self.TYPE_LIMIT
        self.symbol = ''
        self.currency = ''
        self.asset = ''
        self.price = 0
        self.quantity = 0
        self.test = False
        self.created = ''

        for key, value in kwargs.items():
            print("{} is {}".format(key,value))
            setattr(self, key, value)


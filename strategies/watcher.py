from decouple import config
from models import price


def run(newPrice: price.Price):
    print('*******************************')
    print('Exchange: ', newPrice.exchange)
    print('Pair: ', newPrice.pair)
    print('Price: ', newPrice.current)

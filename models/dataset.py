from datetime import datetime

from api import utils
from models.model import AbstractModel
from models.exchange import Exchange
from models.currency import Currency


class Dataset(AbstractModel):
    resource_name = 'datasets'

    pair: str = ''
    exchange: str = ''
    period_start: str = ''
    period_end: str = ''
    currency: str = ''
    asset: str = ''

    relations = {'exchange': Exchange, 'currency': Currency, 'asset': Currency}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pair = self.get_pair()

    def get_pair(self):
        return utils.format_pair(self.currency, self.asset)


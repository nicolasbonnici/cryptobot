from datetime import datetime

from api import utils
from models.model import AbstractModel
from models.exchange import Exchange
from models.currency import Currency


class Dataset(AbstractModel):
    resource_name = 'datasets'

    uuid: str = ''
    pair: str = ''
    exchange: str = ''
    periodStart: datetime
    periodEnd: datetime
    currency: str = ''
    asset: str = ''

    relations = {'exchange': Exchange, 'currency': Currency, 'asset': Currency}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pair = self.get_pair()

    def get_pair(self):
        return utils.format_pair(self.currency, self.asset)


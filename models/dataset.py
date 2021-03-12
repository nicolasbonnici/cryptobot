from datetime import datetime

from api import utils
from models.model import AbstractModel


class Dataset(AbstractModel):
    uuid: str = ''
    pair: str = ''
    exchange: str = ''
    periodStart: datetime
    periodEnd: datetime
    currency: str = ''
    asset: str = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pair = self.get_pair()

    def get_pair(self):
        return utils.format_pair(self.currency, self.asset)

    def get_resource_name(self):
        return 'datasets'

    def serialize(self, data: dict):
        return {**self.__dict__, **data, 'currency': '/api/currencies/' + self.currency.lower(),
                'asset': '/api/currencies/' + self.asset.lower(),
                'exchange': '/api/exchanges/' + self.exchange.lower()}

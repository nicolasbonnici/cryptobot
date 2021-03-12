from api import utils
from models.model import AbstractModel


class Price(AbstractModel):
    dataset: str = ''
    pair: str = ''
    exchange: str = ''
    current: float = 0
    lowest: float = 0
    highest: float = 0
    volume: float = 0
    currency: str = ''
    asset: str = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pair = self.get_pair()

    def get_pair(self):
        return utils.format_pair(self.currency, self.asset)

    def get_resource_name(self):
        return 'prices'

    def serialize(self, data: dict):
        return {**self.__dict__, **data, 'currency': '/api/currencies/' + self.currency,
                'asset': '/api/currencies/' + self.asset, 'exchange': '/api/exchanges/' + self.exchange,
                'dataset': '/api/datasets/' + self.dataset}

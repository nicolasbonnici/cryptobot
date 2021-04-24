from models.model import AbstractModel
from api import utils


class Pair(AbstractModel):
    resource_name = 'pair'

    currency: str = ''
    asset: str = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_symbol(self):
        return utils.format_pair(self.currency, self.asset)

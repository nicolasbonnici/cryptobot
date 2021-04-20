from models.model import AbstractModel

class Pair(AbstractModel):
    resource_name = 'pair'

    currency: str = ''
    asset: str = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_symbol(self):
        return f'{self.currency.upper()}{self.asset.upper()}'



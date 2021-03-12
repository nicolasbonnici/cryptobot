from models.model import AbstractModel


class Currency(AbstractModel):
    name: str = ''
    symbol: str = ''
    fiat: bool

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_resource_name(self):
        return 'currencies'

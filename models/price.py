from models.model import AbstractModel

class Price(AbstractModel):
    uuid = ''
    pair: str = ''
    exchange: str = ''
    current: float = 0
    lowest: float = 0
    highest: float = 0
    currency: str = ''
    asset: str = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

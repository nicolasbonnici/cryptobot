from models.model import AbstractModel


class Order(AbstractModel):
    BUY = 'BUY'
    SELL = 'SELL'

    TYPE_LIMIT = 'LIMIT'
    TYPE_MARKET = 'MARKET'
    TYPE_STOP_LOSS = 'STOP_LOSS'
    TYPE_STOP_LOSS_LIMIT = 'STOP_LOSS_LIMIT'
    TYPE_TAKE_PROFIT = 'TAKE_PROFIT'
    TYPE_TAKE_PROFIT_LIMIT = 'TAKE_PROFIT_LIMIT'
    TYPE_LIMIT_MAKER = 'LIMIT_MAKER'

    uuid = ''
    side: str = ''
    type: str = TYPE_LIMIT
    symbol: str = ''
    currency: str = ''
    asset: str = ''
    price: float = 0
    quantity: int = 0
    test: bool = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

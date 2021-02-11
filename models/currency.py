from decouple import config

class Currency():
    __tablename__ = 'currency'

    uuid = ''
    name = ''
    symbol = ''
    fiat = ''
    created = ''
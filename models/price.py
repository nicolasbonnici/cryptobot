from decouple import config


class Price():
    def __init__(self, uuid='', pair='', exchange='', current=0, lowest=0, highest=0, currency='', asset='', created=''):
        self.uuid = uuid
        self.pair = pair
        self.exchange = exchange
        self.current = current
        self.lowest = lowest
        self.highest = highest
        self.currency = currency
        self.asset = asset
        self.created = created   

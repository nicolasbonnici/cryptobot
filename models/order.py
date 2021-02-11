from decouple import config
import uuid
import datetime


class Order():
    __tablename__ = 'order'

    uuid = ''
    pair = ''
    price = ''
    currency_uuid = ''
    asset_uuid = ''
    quantity = 0
    test = False
    created = ''

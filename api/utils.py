from datetime import datetime


def format_date(date: datetime):
    return date.strftime('%Y-%m-%d %H:%M:%S')


def format_pair(currency: str, asset: str):
    return currency + '_' + asset

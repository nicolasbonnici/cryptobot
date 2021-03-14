from datetime import datetime


def format_date(date: datetime):
    return date.strftime('%Y-%m-%d %H:%M:%S')


def format_pair(currency: str, asset: str):
    return currency + '_' + asset


def filter_keys(data: dict, keys: dict):
    return {k: v for k, v in data.items() if k not in keys}

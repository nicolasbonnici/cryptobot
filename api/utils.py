from datetime import datetime


def format_date(date: datetime):
    return date.strftime('%Y-%m-%d %H:%M:%S')


def format_pair(currency, asset):
    if type(currency) == str and type(asset) is str:
        return currency + '_' + asset
    else:
        return currency.symbol + '_' + asset.symbol


def filter_keys(data: dict, keys: dict):
    return {k: v for k, v in data.items() if k not in keys}

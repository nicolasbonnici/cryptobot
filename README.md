# Crypto bot

Crypto trading bot wrote using Python 3.9. 

- Run your own strategies
- Trade, backtest and live test modes available
- Easily integrate exchanges

More details here on [full project article](https://dev.to/nicolasbonnici/how-to-build-a-crypto-bot-with-python-3-and-the-binance-api-part-1-1864).

## Install and configure project

### Install dependencies

```bash
pip install --no-cache-dir -r requirements.txt
```

### Usage

Configure by creating a .env file from the .env.dist 

```bash
./main.py
```

You can set particular symbol pair by using an argument
```bash
./main.py BTC_EUR
```

You can override any env parameter like so
```bash
MODE=live ./main.py BTC_EUR
```

### Available modes

- "trade" to trade on candlesticks
- "live" to live trade throught WebSocket
- "backtest" to test a strategy for a given symbol pair and a period
- "import" to import dataset from exchanges for a given symbol pair and a period
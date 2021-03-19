# Crypto bot the Binance API. Use Python 3.9

## Install and configure project

## Install dependencies

```bash
pip install --no-cache-dir -r requirements.txt
```

## Usage

Configure you .env.local file

```bash
./main.py
```

You can set particular symbol pair by using an argument
```bash
./main.py BTC_EUR
```

You can override any env parameter like so
```bash
STRATEGY=runner ./main.py BTC_EUR
```

More details here on [full project article](https://dev.to/nicolasbonnici/how-to-build-a-crypto-bot-with-python-3-and-the-binance-api-part-1-1864).

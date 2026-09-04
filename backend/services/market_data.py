import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

FINNHUB_URL = "https://finnhub.io/api/v1/quote"
YAHOO_URL = "https://query1.finance.yahoo.com/v8/finance/chart"

COMPANY_NAMES = {
    "TCS": "Tata Consultancy Services",
    "INFY": "Infosys",
    "RELIANCE": "Reliance Industries",
    "HDFCBANK": "HDFC Bank",
    "AAPL": "Apple Inc.",
}

FINNHUB_SYMBOLS = {
    "TCS": "NSE:TCS",
    "INFY": "NSE:INFY",
    "RELIANCE": "NSE:RELIANCE",
    "HDFCBANK": "NSE:HDFCBANK",
}

YAHOO_SYMBOLS = {
    "TCS": "TCS.NS",
    "INFY": "INFY.NS",
    "RELIANCE": "RELIANCE.NS",
    "HDFCBANK": "HDFCBANK.NS",
}


def get_from_finnhub(symbol: str):
    if not FINNHUB_API_KEY:
        return None

    try:
        finnhub_symbol = FINNHUB_SYMBOLS.get(symbol, symbol)

        response = requests.get(
            FINNHUB_URL,
            params={
                "symbol": finnhub_symbol,
                "token": FINNHUB_API_KEY,
            },
            timeout=5,
        )

        response.raise_for_status()

        data = response.json()
        price = data.get("c")

        if not price or price == 0:
            return None

        return {
            "symbol": symbol,
            "company_name": COMPANY_NAMES.get(symbol, symbol),
            "price": price,
            "volume": None,
            "timestamp": datetime.now(timezone.utc),
            "source": "Finnhub",
        }

    except requests.RequestException:
        return None


def get_from_yahoo(symbol: str):
    try:
        yahoo_symbol = YAHOO_SYMBOLS.get(symbol, symbol)

        response = requests.get(
            f"{YAHOO_URL}/{yahoo_symbol}",
            params={
                "range": "1d",
                "interval": "1m",
            },
            timeout=5,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
        )

        response.raise_for_status()

        data = response.json()
        result = data["chart"]["result"][0]

        meta = result["meta"]

        price = meta.get("regularMarketPrice")

        if not price or price == 0:
            return None

        volume = meta.get("regularMarketVolume")

        timestamp = datetime.fromtimestamp(
            meta.get("regularMarketTime"),
            tz=timezone.utc
        ) if meta.get("regularMarketTime") else datetime.now(timezone.utc)

        return {
            "symbol": symbol,
            "company_name": COMPANY_NAMES.get(symbol, symbol),
            "price": price,
            "volume": volume,
            "timestamp": timestamp,
            "source": "Yahoo Finance",
        }

    except (requests.RequestException, KeyError, IndexError, TypeError):
        return None


def get_market_data(symbol: str):
    """
    Fetch market data using Finnhub as the primary provider
    and Yahoo Finance as a fallback provider.
    """

    symbol = symbol.upper()

    # Primary provider
    data = get_from_finnhub(symbol)

    if data:
        return data

    # Fallback provider
    return get_from_yahoo(symbol)
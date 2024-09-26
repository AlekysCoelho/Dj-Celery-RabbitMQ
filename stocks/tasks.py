import logging
from datetime import datetime
from time import sleep

import pytz
import yfinance as yf
from celery import shared_task

from stocks.models import Stock

logger = logging.getLogger(__name__)


def get_stock(data):
    """Search Yahoo Finance API for some information about given ticker."""
    logger.info(f"Processing ticker in get_stock: {data}")
    ticker = yf.Ticker(data)
    current_price = ticker.info.get("currentPrice")
    current_open = ticker.info.get("open")
    pe_ratio = ticker.info.get("trailingPE")
    if pe_ratio:
        pe_ratio = round(pe_ratio, ndigits=2)

    return ticker, current_price, current_open, pe_ratio


@shared_task
def api_stock(data):
    """Feeds the Stock Model with the information retrieved by the get_stock() function and saves it in the database."""
    logger.info(f"Processing ticker in api_stock: {data}")

    ticker, current_price, current_open, pe_ratio = get_stock(data)

    Stock.objects.create(
        ticker=ticker.ticker,
        current_price=current_price,
        current_open=current_open,
        pe_ratio=pe_ratio,
    )

    return f"{ticker} - {current_price}"


@shared_task
def update_tickers_everyday():
    """Makes a daily update of the tickers already registered."""

    stocks_update = []

    stocks = Stock.objects.all()
    for stock in stocks:
        logger.info(f"Processing ticker in api_stock: {stock.ticker}")
        ticker, current_price, current_open, pe_ratio = get_stock(stock.ticker)
        stock.ticker = ticker.ticker
        stock.current_price = current_price
        stock.current_open = current_open
        stock.pe_ratio = pe_ratio
        stock.moment = datetime.now(pytz.utc)
        stocks_update.append(stock)
        sleep(10)

    Stock.objects.bulk_update(
        stocks_update, ["ticker", "current_price", "current_open", "pe_ratio", "moment"]
    )

    return "UPDATE TICKERS DONE!"

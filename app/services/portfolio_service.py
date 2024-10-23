import requests
from functools import reduce
from app.models.Transaction import Transaction
from app.repositories.transaction_repo import get_transactions_by_user_id
from app.services.crypto_service import get_crypto_price
from datetime import datetime, timedelta

COINGECKO_HISTORICAL_PRICE_URL = "https://api.coingecko.com/api/v3/coins/{}/history"


def calculate_portfolio_value(user_id):
    transactions = get_transactions_by_user_id(user_id)

    filtered_transactions = list(filter(lambda t: t.transaction_type in ['buy', 'sell'], transactions))

    mapped_transactions = list(map(lambda t:
                                   t.amount * get_crypto_price(t.cryptocurrency)
                                   if t.transaction_type == 'buy'
                                   else -t.amount * get_crypto_price(t.cryptocurrency),
                                   filtered_transactions))

    total_value = reduce(lambda x, y: x + y, mapped_transactions, 0)

    return {"total_value": total_value}


def get_portfolio_summary(user_id):
    transactions = get_transactions_by_user_id(user_id)

    cryptos = set(t.cryptocurrency for t in transactions)

    prices = {crypto: get_crypto_price(crypto) for crypto in cryptos}

    portfolio = {}
    for transaction in transactions:
        crypto = transaction.cryptocurrency
        if crypto not in portfolio:
            portfolio[crypto] = {
                "amount": 0,
                "purchase_value": 0,
                "current_value": 0
            }

        if transaction.transaction_type == 'buy':
            portfolio[crypto]["amount"] += transaction.amount
            portfolio[crypto]["purchase_value"] += transaction.amount * transaction.transaction_price
        elif transaction.transaction_type == 'sell':
            portfolio[crypto]["amount"] -= transaction.amount
            portfolio[crypto]["purchase_value"] -= transaction.amount * transaction.transaction_price

        portfolio[crypto]["current_value"] = portfolio[crypto]["amount"] * prices[crypto]

    return portfolio


def get_crypto_historical_price(crypto_id, date):

    formatted_date = date.strftime('%d-%m-%Y')
    response = requests.get(COINGECKO_HISTORICAL_PRICE_URL.format(crypto_id),
                            params={'date': formatted_date, 'localization': 'false'})
    if response.status_code == 200:
        data = response.json()
        if 'market_data' in data and 'current_price' in data['market_data']:
            return data['market_data']['current_price']['usd']
        else:
            raise Exception(f"Historical price data for {crypto_id} not found.")
    else:
        raise Exception(f"Error fetching historical price data: {response.status_code}")


def calculate_portfolio_value_for_date(user_id, date):
    """
    Calculate the portfolio value for a specific date.
    This involves querying transactions and getting the prices
    of the cryptocurrencies as they were on that date.
    """
    transactions = get_transactions_by_user_id(user_id)
    total_value = 0

    for transaction in transactions:
        if transaction.transaction_date <= date:
            try:
                historical_price = get_crypto_historical_price(transaction.cryptocurrency, date)
                if transaction.transaction_type == 'buy':
                    total_value += transaction.amount * historical_price
                else:
                    total_value -= transaction.amount * historical_price
            except Exception as e:
                print(e)

    return total_value


def get_historical_portfolio_values(user_id, days=30):
    """
    Get historical portfolio values for the last 'days' days.
    """
    historical_values = []
    end_date = datetime.utcnow()

    for day in range(days):
        date = end_date - timedelta(days=day)
        value = calculate_portfolio_value_for_date(user_id, date)
        historical_values.append({"date": date.strftime('%Y-%m-%d'), "value": value})

    return historical_values

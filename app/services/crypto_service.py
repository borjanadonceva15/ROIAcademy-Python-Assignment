import requests

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"


def get_crypto_price(crypto_id):
    response = requests.get(f"{COINGECKO_API_URL}?ids={crypto_id}&vs_currencies=usd")
    if response.status_code == 200:
        data = response.json()
        if crypto_id in data:
            return data[crypto_id]['usd']
        else:
            raise Exception(f"Crypto ID {crypto_id} not found in CoinGecko API response.")
    else:
        raise Exception(f"Error fetching data from CoinGecko API: {response.status_code}")


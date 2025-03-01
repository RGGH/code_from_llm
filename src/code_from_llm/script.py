import requests
import json

def get_bitcoin_price():
    URL = "https://api.gemini.com/v1/pubticker/btcusd"
    response = requests.get(url=URL)
    data = json.loads(response.text)
    return data['last']

print(get_bitcoin_price())
from requests import get
import json

def exchange(usd:float)->float:
    url = "https://raters.ir/exchange/api/currency/usd"
    response = get(url)
    data = json.loads(response.text)
    price = data["data"]["prices"][0]["live"]
    price = price.replace(",",'')
    price = int(price)
    return usd*price

if __name__ == "__main__":
    result = exchange(1)
    print(result)

from requests import get
import json
from bs4 import BeautifulSoup

def exchange(usd:float)->float:
    url = "https://www.tgju.org/profile/price_dollar_rl"
    response = get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    result = soup.select("div.col-lg-12:nth-child(1) > div:nth-child(1) > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)")
    result = result[0].text
    price = result.replace(",",'')
    price = int(price)
    return usd*price

if __name__ == "__main__":
    result = exchange(1)
    print(result)

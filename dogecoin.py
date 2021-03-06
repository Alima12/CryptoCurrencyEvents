from requests import get
from bs4 import BeautifulSoup
from usd_rial import exchange


def doge_price_now()-> tuple:
    url = "https://arzdigital.com/coins/dogecoin/"
    response = get(url)
    soup = BeautifulSoup(response.content,"html.parser")
    result = soup.select("#coin-details-page > section.arz-coin-page-body > div.arz-coin-page-data > div.arz-row-sb.arz-coin-page-data__gen-info > div:nth-child(2) > div.arz-row.arz-coin-page-data__info > div.arz-col-12.arz-col-sm-6 > div.arz-coin-page-data__coin-price-box > div:nth-child(2) > div.arz-coin-page-data__coin-price.coinPrice.pulser")
    usd_rial_price = exchange(1)
    doge_usd = float(result[0].text.replace("$",""))
    doge_rial = round(doge_usd*usd_rial_price,2)
    return (doge_rial,doge_usd)



if __name__ == "__main__":
    print(doge_price_now())

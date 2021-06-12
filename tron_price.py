
from requests import Request, Session,get
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from bs4 import BeautifulSoup


def tron_price_now():
    url = "https://www.tgju.org/profile/crypto-tron"
    response = get(url)
    soup = BeautifulSoup(response.content,"html.parser")
    selected_area = soup.select("#main > div.stocks-profile > div.fs-row.bootstrap-fix.widgets.full-w-set > div > div.tgju-widgets-block.col-md-12.col-lg-4.tgju-widgets-block-bottom-unset.overview-first-block > div > div:nth-child(1) > div > div.tables-default.normal > table > tbody > tr:nth-child(2) > td.text-left")
    tron_rial = int(selected_area[0].text.replace(',',''))
    selected_area = soup.select("#main > div.stocks-profile > div.stocks-header > div.stocks-header-main > div > div.fs-cell.fs-xl-3.fs-lg-3.fs-md-6.fs-sm-12.fs-xs-12.top-header-item-block-2.mobile-top-item-hide > div > div.line.clearfix.mobile-hide-block > span.value > span:nth-child(1)")
    tron_usd = float(selected_area[0].text)
    return (tron_rial,tron_usd)

if __name__ == "__main__":
    print(tron_price_now())
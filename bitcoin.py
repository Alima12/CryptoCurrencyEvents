import requests as req



def get_bitcoin_price():
    url = "https://blockchain.info/ticker"
    response = req.get(url)
    response = response.json()
    #جدا کردن قیمت دلاری
    price = response["USD"]
    #گرفتن قیمت خرید بیت کوین
    buy_price = price["buy"]

    return buy_price
    # لیست پیام ها که در صورتی که رویدادی رخ نداده باشد تعداد اعضای آن یک میباشید
    
    
   


if __name__ == "__main__":
    set_price()

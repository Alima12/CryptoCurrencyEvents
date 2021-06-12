from tron_price import tron_price_now
from usd_rial import exchange
from connectToDb import insert,Least,Most,min_max_today,min_max_yesterday,growth
from telebot import send_notification
from dogecoin import doge_price_now
from bitcoin import get_bitcoin_price

def get_growth(price:int,symbol:str) -> str:
    days = [0,2,3,7,15,30]
    text = "\n\n⚡️میزان رشد:\n\n"
    #فقط متن ارسالی را زیبا میکنه
    def change_form(dif:str) ->str:
        dif = str(dif)
        if '-' in dif:
            dif = dif.replace('-','')
            dif = dif + '➖ '
        else:
            dif = dif +  "➕ " 

        return dif
    
    #سه بازه زمانی 3,7 و 30 رو بررسی میکنه و درصد رشدشون رو محسابه میکنه
    for day in days:
        dif = growth(day,price,symbol)
        if day == 0:
            dif = change_form(dif)
            t= f"☀️ امروز => %{dif}\n"
        else:
            dif = change_form(dif)
            t= f"📊 از {day} روز پیش => %{dif}\n"
        text += t
    return text


def check_events()->list:
    days = [2,3,7,15,30]
    event_list = []
    for coin in Coins.keys():
        this = Coins[coin]
        name = this["name"]
        rial= this["rial"]
        usd = this["usd"]
        icon = this["icon"]
        event = list()
        event.append(f"{icon}بررسی قیمت {name} در این لحظه\n")
        for period in days:
            if Least(coin,rial,period):
                event.append(f"🔔🔴کمترین قیمت در {period} روز اخیر")
            elif Most(coin,rial,period):
                event.append(f"🔔🟢بیشترین قیمت در  {period} روز اخیر")
        
        min,max= min_max_today(coin)
        try:
            if len(event) > 1 or (min>rial) or (max<rial):
                min /= 10
                max /= 10
                now = rial / 10
                event.append("\nتغییرات قیمت امروز📊")
                event.append("*قیمت ها به تومان میباشد")
                event.append(f"🔴کمترین قیمت: {min:,}\n⚪️قیمت کنونی: {now:,}\n🟢بیشترین قیمت: {max:,}\n")
                event.append(f"""💰قیمت دلاری {name}: {usd:,}
💶قیمت دلار : {usd_rial_price}""")
                event.append(get_growth(rial,coin))
                event.append("\n🆔 @CryptoCurrency_Events")
                event_list.append(event)
        except:
            print("Error in finding max annd min price for today")
    if len(event_list) > 0:
        return event_list









    return False
    



def set_price()->list:
    events = check_events()
    insert("TRX",tron_usd,tron_rial)
    insert("DOGECOIN",doge_usd,doge_rial)
    insert("BITCOIN",bitcoin_usd,bitcoin_rial)


    if events:
        return events
    return False


tron_rial,tron_usd= tron_price_now()
doge_rial,doge_usd= doge_price_now()
usd_rial_price = exchange(1) *0.1
bitcoin_usd = get_bitcoin_price()
bitcoin_rial = bitcoin_usd * (usd_rial_price * 10)
Coins ={
    "TRX":{
        "name":"ترون",
        "rial":tron_rial,
        "usd":tron_usd,
        "icon":"🔰"
    },
    "DOGECOIN":{
        "name":"دوج کوین",
        "rial":doge_rial,
        "usd":doge_usd,
        "icon":"🐶"
    },
    "BITCOIN":{
        "name":"بیتکوین",
        "rial":bitcoin_rial,
        "usd":bitcoin_usd,
        "icon":"💎"
    }
}



events = set_price()
if events:
    for event in events:
        message = "\n".join(event)
        send_notification(message)
else:
    print("no Changes!.")






import sqlite3
from datetime import datetime,timedelta

connect = sqlite3.connect("dataprices.db")
cursor = connect.cursor()
#چک میکنه اگر جدول در پایگاه داده وجود نداشته باشد آن را میسازد
def create():
    q = """create table if not exists Prices(
        symbol VACHAR,
        usd_price INT,
        rial_price INT,
        record DATETIME NOT NULL default CURRENT_TIMESTAMP
    );"""
    cursor.execute(q)

#برای افزودن یک ردیف به جدول قیمت ها
def insert(symbol:str,usd:float,rial:int):
    time = datetime.now().strftime("%y/%m/%d %H:%M:%S")
    q = f"""INSERT INTO Prices VALUES("{symbol}",{usd},{rial},'{time}');"""
    cursor.execute(q)
    connect.commit()

#گرفتن کمترین قیمت در بازه های زمانی مختلف
#روز و قیمت را میگیرد
#True = کمترین قیمت در بازه زمانی گرفته شده
def Least(symbol:str,rial:float,day:int) -> bool:
    time = datetime.now() - timedelta(day)
    time = time.strftime("%y/%m/%d %H:%M:%S")
    q = f"""SELECT count(*) FROM Prices where record >= "{time}" and rial_price <= {rial} and symbol = '{symbol}'; """
    res = cursor.execute(q)
    for item in res:
        count = item[0]
    if count == 0:
        return True
    return False


#گرفتن بیشترین قیمت در بازه های زمانی مختلف
#روز و قیمت را میگیرد
#True = بیشترین قیمت در بازه زمانی گرفته شده
def Most(symbol:str,rial:float,day:int) ->bool:
    time = datetime.now() - timedelta(day)
    time = time.strftime("%y/%m/%d %H:%M:%S")
    q = f"""SELECT count(*) FROM Prices where record >= "{time}" and rial_price >= {rial} and symbol = '{symbol}'; """
    res = cursor.execute(q)
    for item in res:
        count = item[0]
    if count == 0:
        return True
    return False

#کمترین و بیشترین قیمت امروز را برمیگرداند
def min_max_today(symbol:str) ->float:
    time = datetime.now()
    begin = time.strftime("%y/%m/%d 00:00:00")
    end =  time.strftime("%y/%m/%d 23:59:59")
    q= f"SELECT min(rial_price),max(rial_price) FROM Prices WHERE '{begin}'  <= record AND record <= '{end}' and symbol = '{symbol}';"
    res = cursor.execute(q)
    for row in res:
        if row[0] and row[1]:
            return row
        else:
            return (0,0)
#کمترین و بیشترین قیمت دیروز را برمیگرداند
def min_max_yesterday(symbol:str) ->float:
    time = datetime.now() - timedelta(1)
    begin = time.strftime("%y/%m/%d 00:00:00")
    end =  time.strftime("%y/%m/%d 23:59:59")
    q= f"SELECT min(rial_price),max(rial_price) FROM Prices WHERE '{begin}'  <= record AND record <= '{end}' and symbol = '{symbol}';"
    res = cursor.execute(q)
    for row in res:
        if row[0] and row[1]:
            return row
        else:
            return (0,0)

#درصد رشد را محاسبه میکند
def growth(day:int,price:float,symbol:str) -> float:
    time = datetime.now() - timedelta(day)
    begin = time.strftime("%y/%m/%d 00:00:00")
    end =  time.strftime("%y/%m/%d 23:59:59")
    q= f"SELECT rial_price FROM Prices Where record < '{end}' and record >  '{begin}' and symbol = '{symbol}' ORDER BY record LIMIT 1;"
    res = cursor.execute(q)
    past = 0
    for row in res:
        past = row[0]
    if past > 0:
        dif = (price - past) / past * 100
        dif = round(dif,2)
    else:
        dif = 0
    return dif

#رکورد های ۶ ساعت اخیر را به صورت لیست برمیگرداند
#فقط قیمت خرید را برمیگرداند
# قیمت ها را تقسیم بر هزار میکند برای یهتر نشان دادن نمودار
def data() -> list:
    time = datetime.now() - timedelta(hours=6)
    time = time.strftime("%y/%m/%d %H:%M:%S")
    q = f"""SELECT buy FROM Prices where sec >= "{time}"; """
    res = cursor.execute(q)
    data_chart= []
    for item in res:
        data_chart.append(item[0]/ 1000.0)
    return data_chart
    


create()





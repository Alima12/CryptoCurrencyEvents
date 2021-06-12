from telegram.ext import Updater
 


updater = Updater(token='1872145344:AAFX5SUhF4QrIh4ud8s6KXwP0i0xumxyhCg', use_context=True)
bot = updater.bot

reciver_list = ("@CryptoCurrency_Events",)


def send_notification(message:str)->None:
    for user in reciver_list:
            bot.send_message(user,message)
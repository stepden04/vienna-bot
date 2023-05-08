from telebot import TeleBot
from schedule import every, run_pending,repeat
from threading import Thread
from time import sleep
from dotenv import dotenv_values

API_TOKEN = dotenv_values()['TOKEN']
CHANNEL_ID = dotenv_values()['CHANNEL']

bot = TeleBot(API_TOKEN, parse_mode=None) # bot init

# TODO store in file
previous_titles = set() # better then list to store unique items

@bot.message_handler(commands=['start', 'help'])
def send_start(message):
    bot.reply_to(message, 'cum')



if __name__ == '__main__':
    bot_polling = Thread(target=bot.infinity_polling)
    bot_polling.start()
    while True:
        run_pending()
        sleep(1)
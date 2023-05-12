from telebot import TeleBot
from schedule import every, run_pending,repeat
from multiprocessing import Process
from time import sleep
from dotenv import dotenv_values
from signal import signal, SIGINT
from sys import exit
from db import close_db


API_TOKEN = dotenv_values()['TOKEN']
CHANNEL_ID = dotenv_values()['CHANNEL']

bot = TeleBot(API_TOKEN, parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_start(message):
    bot.reply_to(message, 'cum')

def kill_bot(signal_received, frame):
    print('Killing bot, saving database')
    close_db()
    print('Saved database')
    bot_polling.kill()
    exit(0)

if __name__ == '__main__':
    signal(SIGINT, kill_bot)

    bot_polling = Process(target=bot.infinity_polling)
    bot_polling.start()
    while True:
        run_pending()
        sleep(1)
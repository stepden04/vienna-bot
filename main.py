from telebot import TeleBot
from telebot.types import InputMediaPhoto
import telebot
from schedule import every, run_pending,repeat
from multiprocessing import Process
from time import sleep
from dotenv import dotenv_values
from signal import signal, SIGINT
from sys import exit
from db import close_db, is_listed, append_db,update_value
from request import get_json_listings,get_listings
from page import Listing
from requests import Session

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

@repeat(every(15).minutes)
def update():
    
    listings_json = get_json_listings(Session())
    listings_tuple = get_listings(listings_json)
    listings = []
    
    for listing in listings_tuple:
        listings.append(Listing(listing[0],listing[1],download=False))

    for listing in listings: 
        if not is_listed(listing.uri): 
            append_db(listing.title,listing.uri,1)
            
            media = []
            for i in range(listing.links):
                media.append(InputMediaPhoto(listing.links[i]))
            media[0].caption = listing.compose()
            
            bot.send_media_group(chat_id=CHANNEL_ID,media=media)
            
if __name__ == '__main__':
    signal(SIGINT, kill_bot)

    bot_polling = Process(target=bot.infinity_polling)
    bot_polling.start()
    while True:
        run_pending()
        sleep(1)
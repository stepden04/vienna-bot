from telebot import TeleBot, types
from schedule import every, run_pending,repeat
from threading import Thread
from time import sleep
from dotenv import dotenv_values
from page import init_titles_file,Listing
types.Message.parse_photo()
config = dotenv_values()

bot = TeleBot(config['TOKEN'], parse_mode=None) # bot init

PREVIOUS_LISTINGS = init_titles_file(config["TITLES_PATH"])


@bot.message_handler(commands=['start', 'help'])
def send_start(message):
    try:
        bot.reply_to(message, 'cum')
    except:
        print('Failed to send a message in send_start()')


@repeat(every(15).minutes)
def update_feed(listing):
    if check_new_listings():
        send_listing(listing)
        PREVIOUS_LISTINGS.add(listing)

@repeat(every(10).seconds)
def test():
    try:
        bot.send_message(chat_id=config['CHANNEL'],text='cum')
    except:
        print('Failed to send a message test()')

def check_new_listings():
    NotImplemented

def is_listed(listing):
    return listing in PREVIOUS_LISTINGS

def send_listing(listing : Listing):
    try:        
        bot.send_media_group(config['CHANNEL'],media=listing.photos_raw)
    except:
        print('Cant add images')
        try:
            bot.send_message(config['CHANNEL'],text=listing.compose())
        except:
            print('Cant send a message in send_listing()')

if __name__ == '__main__':
    bot_polling = Thread(target=bot.infinity_polling)
    bot_polling.start()
    while True:
        run_pending()
        sleep(1)
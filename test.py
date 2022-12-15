from datetime import date, datetime
from tzlocal import get_localzone
from dbconnect import get_data, get_data_line, insert
import difflib

def similarity(s1, s2):
    normalized1 = s1.lower()
    normalized2 = s2.lower()
    matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
    return matcher.ratio()

#res = similarity('Китайский хлебный братец кормит чаек плащом и короной из булочек', '«Братец-хлеб» из Китая носит плащ и корону из булочек, чтобы кормить чаек')
#print(res)

import configparser
from telethon import TelegramClient, events

config = configparser.ConfigParser()
config.read("data.ini")

# Присваиваем значения внутренним переменным
api_id   = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']
channel_id = config['Telegram_bot']['channel_id']

client = TelegramClient('session_read', api_id, api_hash)

@client.on(events.NewMessage)
async def my_event_handler(event):
    if hasattr(event.message.to_id, 'channel_id'):
        if (event.message.to_id.channel_id == channel_id[4:]):
            print('Соо')
        print('{}'.format(event.message))
    else:
        print('Сообщение пользователя')

client.start()
client.run_until_disconnected()

import configparser
import asyncio

from dbconnect import insert_posts, insert
from telethon import TelegramClient, events
from tzlocal import get_localzone

tz = get_localzone()

def telegram_listening():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

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
        try:
            if hasattr(event.message.to_id, 'channel_id'):
                if (int(event.message.to_id.channel_id) == int(channel_id[4:])):
                    print('Сообщение из своей группы', event.message.chat.username)
                else:
                    #insert_posts(all_messages, name_channel
                    sql = "INSERT INTO posts (id_telegram_post, channel, media, text, date, verified) VALUES (?, ?, ?, ?, ?, 'f')"
                    insert(sql, (event.message.id, 'https://t.me/{}'.format(event.message.chat.username), str(event.message.media), event.message.message, event.message.date.astimezone(tz), ))
                    sql2 = "INSERT INTO posts_json (json, date) VALUES (?, ?)"
                    insert(sql2, ('{}'.format(event.message), event.message.date.astimezone(tz), ))
                    print('{}'.format(event.message))
                    print(event.message.chat.username)
            else:
                print('Сообщение пользователя')
                print(event.message.chat.username)
        except Exception as ex:
            print(ex)

    client.start()
    client.run_until_disconnected()
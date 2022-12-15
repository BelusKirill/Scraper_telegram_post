import datetime
import os
import subprocess
import threading

from configparser import ConfigParser
from body_bot import dp
from aiogram.utils import executor
from aiogram import Dispatcher
from loader import scheduler #pip install apscheduler
from dbconnect import get_data, insert

config = ConfigParser()
config.read('data.ini')

job_active = False

async def generate_sources(array):
    sources = set()
    msg = "\n\nИсточники:\n"

    for row in array:
        sources.add(row[1])

    for item in sources:
        msg += item
        msg += "\n"
    
    return msg

async def send_posts(dp: Dispatcher):
    try:
        sql = "SELECT id FROM for_post WHERE sent = 'f'"
        data = get_data(sql)
        if data == None: return
        for id in data:
            msg = None

            sql2 = f"SELECT b.* FROM channels a INNER JOIN posts b on a.id_for_post = {id[0]} and b.id = a.id_post ORDER BY b.date DESC"
            data2 = get_data(sql2)
            try:
                msg = data2[0][3]
            except: continue
            msg += await generate_sources(data2)

            if msg != None:
                await dp.bot.send_message(config['Telegram_bot']['channel_id'], msg)
            else: continue

            sql3 = f"UPDATE for_post SET sent = 't' WHERE id = {id[0]}"
            insert(sql3)
    except Exception as ex:
        print(ex)

async def send_message_to_user(dp: Dispatcher):
    global job_active

    if job_active == True: return

    job_active = True
    try:
        date = datetime.datetime.now()

        if (date.time().hour == 9 and date.time().minute == 0):
            print(date.time().hour, date.time().minute)
            os.system("start cmd /k python main.py")
            await send_posts(dp)
        elif (date.time().hour == 14 and date.time().minute == 0):
            print(date.time().hour, date.time().minute)
            os.system("start cmd /k python main.py")
            await send_posts(dp)
        elif (date.time().hour == 21 and date.time().minute == 30):
            print(date.time().hour, date.time().minute)
            os.system("start cmd /k python main.py")
            await send_posts(dp)
        else:
            print(date.time().hour, date.time().minute)
            await send_posts(dp)
    except Exception as ex:
        print(ex)
    finally:
        job_active = False

def scheduler_jods():
    scheduler.add_job(send_message_to_user, "interval", seconds=60, args=(dp,))


async def startup(dp: Dispatcher) -> None: # запускаем таски executor.start_polling(dp, on_startup=startup)
    scheduler_jods()
    print('Starting bot {}'.format(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")))

def run_scraper():
    print('test')

if __name__ == '__main__':
    thread = threading.Thread(target=run_scraper)
    thread.start()

    scheduler.start()
    executor.start_polling(dp, on_startup=startup)
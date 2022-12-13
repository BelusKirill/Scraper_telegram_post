import datetime

from body_bot import dp
from aiogram.utils import executor
from aiogram import Dispatcher
from loader import scheduler #pip install apscheduler

async def send_message_to_user(dp: Dispatcher):
    print(datetime.datetime.now().time().hour, datetime.datetime.now().time().minute)
    await dp.bot.send_message(-1001804779789, '22')
    #for id_chat in dirt:
        #print(id_chat)
        #await dp.bot.send_message(id_chat, dirt[id_chat])
        #await dp.bot.edit_message_text(chat_id=id_chat, message_id=dirt[id_chat], text=str(i))

def scheduler_jods():
    scheduler.add_job(send_message_to_user, "interval", seconds=60, args=(dp,))


async def startup(dp: Dispatcher) -> None: # запускаем таски executor.start_polling(dp, on_startup=startup)
    scheduler_jods()
    print('Starting bot {}'.format(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")))

if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, on_startup=startup)
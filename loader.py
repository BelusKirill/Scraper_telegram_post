from sched import scheduler
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from configparser import ConfigParser

config = ConfigParser()
config.read('data.ini')
config_telegram = config['Telegram_bot']

bot = Bot(token=config_telegram['token'], parse_mode=types.ParseMode.HTML)
mstorage = MemoryStorage()
dp = Dispatcher(bot, storage=mstorage)
scheduler = AsyncIOScheduler()
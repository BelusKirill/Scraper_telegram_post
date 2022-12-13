from configparser import ConfigParser
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

config = ConfigParser()
config.read('data.ini')
config_telegram = config['Telegram_bot']

bot = Bot(token=config_telegram['token'])
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
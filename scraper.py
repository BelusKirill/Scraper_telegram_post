import configparser
import json

from telethon.sync import TelegramClient
from telethon import connection

# для корректного переноса времени сообщений в json
from datetime import date, datetime

# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest

from calc import check_data

class DateTimeEncoder(json.JSONEncoder):
	'''Класс для сериализации записи дат в JSON'''
	def default(self, o):
		if isinstance(o, datetime):
			return o.isoformat()
		if isinstance(o, bytes):
			return list(o)
		return json.JSONEncoder.default(self, o)

def run_scraper(name_channel: str):
	# Считываем учетные данные
	config = configparser.ConfigParser()
	config.read("data.ini")

	# Присваиваем значения внутренним переменным
	api_id   = config['Telegram']['api_id']
	api_hash = config['Telegram']['api_hash']
	username = config['Telegram']['username']

	# Прокси
	"""
	proxy = (proxy_server, proxy_port, proxy_key)

	client = TelegramClient(username, api_id, api_hash,
		connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,
		proxy=proxy)
	"""
	client = TelegramClient(username, api_id, api_hash)

	client.start()

	async def dump_all_messages(channel):
		"""Записывает json-файл с информацией о всех сообщениях канала/чата"""
		offset_msg = 0    # номер записи, с которой начинается считывание
		limit_msg = 100   # максимальное число записей, передаваемых за один раз

		all_messages = []   # список всех сообщений
		total_messages = 0
		total_count_limit = 0  # поменяйте это значение, если вам нужны не все сообщения

		while True:
			check = True
			history = await client(GetHistoryRequest(
				peer=channel,
				offset_id=offset_msg,
				offset_date=None, add_offset=0,
				limit=5, max_id=0, min_id=0,
				hash=0))
			if not history.messages:
				break
			messages = history.messages
			for message in messages:
				check = check_data(message.date)
				if (check):
					all_messages.append(message.to_dict())
				else: 
					break
			offset_msg = messages[len(messages) - 1].id
			total_messages = len(all_messages)
			if total_count_limit != 0 and total_messages >= total_count_limit or not check:
				break

		with open('channel_messages.json', 'w', encoding='utf8') as outfile:
			json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)
			print(f'Записанно {len(all_messages)} постов из канала {name_channel}')


	async def scraper():
		try:
			#url = input("Введите ссылку на канал или чат: ")
			print(f'Начало чтение постов из {name_channel}')
			channel = await client.get_entity(name_channel)
			await dump_all_messages(channel)
		except Exception as ex:
			print(ex)


	with client:
		client.loop.run_until_complete(scraper())
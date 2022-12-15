import threading
import bot
import scraper
import manager_generating_message_to_send as gms

from bot import start_bot
from calc import checking_uniqueness
from dbconnect import get_data, insert, insert_get_id

def save_channels_to_database():
    thread_scraper = threading.Thread(target=scraper.telegram_listening)
    thread_scraper.start()

    thread_schedule = threading.Thread(target=gms.start_schedule)
    thread_schedule.start()

    start_bot()

save_channels_to_database()
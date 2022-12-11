from scraper import run_scraper
from calc import checking_uniqueness
from dbconnect import get_data

names_channel = []
channels = []

with open("channel_list.txt", "r") as file:
    for line in file:
        try:
            name_channel = line.replace('\n','')
            run_scraper(name_channel)
            channels.append(get_data(f"SELECT id, text FROM posts WHERE channel = '{name_channel}' and verified = 'f'"))
            names_channel.append(name_channel)
        except Exception as ex:
            print(ex)

checking_uniqueness(channels, names_channel)
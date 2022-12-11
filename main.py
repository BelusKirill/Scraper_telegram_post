from scraper import run_scraper
from dbconnect import get_data

name_channels = {}

with open("channel_list.txt", "r") as file:
    for line in file:
        try:
            name_channel = line.replace('\n','')
            run_scraper(name_channel)
            name_channels[name_channel] = get_data(f"SELECT id, text FROM posts WHERE channel = '{name_channel}' and verified = 'f'")
        except Exception as ex:
            print(ex)

print(name_channels['https://t.me/breakingmash'])
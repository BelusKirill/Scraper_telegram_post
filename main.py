from scraper import run_scraper
from calc import checking_uniqueness
from dbconnect import get_data, insert, insert_get_id

names_channel = []
channels = []

with open("channel_list.txt", "r") as file:
    for line in file:
        try:
            name_channel = line.replace('\n','')
            #run_scraper(name_channel)
            channels.append(get_data(f"SELECT id, text, verified FROM posts WHERE channel = '{name_channel}' and verified = 'f'"))
            names_channel.append(name_channel)
        except Exception as ex:
            print(ex)

groups_for_post = checking_uniqueness(channels, names_channel)

try:
    for group in groups_for_post:
        sql = "INSERT INTO for_post (sent) VALUES ('f')"
        id = insert_get_id(sql)
        if (id == None): continue

        for id_post in group:
            sql2 = f"INSERT INTO channels (id_for_post, id_post) VALUES ({id}, {id_post})"
            insert(sql2)
            sql3 = f"UPDATE posts SET verified = 't' WHERE rowid = {id_post}"
            insert(sql3)
except Exception as ex:
    print(ex)
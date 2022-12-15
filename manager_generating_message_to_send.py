import schedule
import time

from datetime import datetime
from dbconnect import get_data, insert, insert_get_id
from calc import checking_uniqueness

def generate_list_to_send():
    print(f'Начало алгоритма формирования списка постов для отправки. Время:{datetime.now()}')
    array_channels = []

    sql = "SELECT DISTINCT channel FROM posts WHERE verified = 'f'"
    channels = get_data(sql)

    if channels != None:
        for channel in channels:
            try:
                if len(channel) == 0: continue
                if not str(channel[0]).startswith("https://t.me/"): 
                    sql_set_t = f"UPDATE posts SET verified = 't' WHERE channel = ?"
                    insert(sql_set_t, (channel[0], ))
                    continue
                if str(channel[0]).endswith("None"):
                    sql_set_t = f"UPDATE posts SET verified = 't' WHERE channel = ?"
                    insert(sql_set_t, (channel[0], )) 
                    continue

                print(channel[0])
                array_channels.append(get_data(f"SELECT id, text, verified FROM posts WHERE channel = '{channel[0]}' and verified = 'f'"))
            except Exception as ex:
                print(ex)
                continue

    groups_for_post = checking_uniqueness(array_channels)
    count_post = 0

    try:
        if groups_for_post != None:
            for group in groups_for_post:
                sql = "INSERT INTO for_post (sent) VALUES ('f')"
                id = insert_get_id(sql)
                if (id == None): continue

                for id_post in group:
                    sql2 = f"INSERT INTO channels (id_for_post, id_post) VALUES ({id}, {id_post})"
                    insert(sql2, ())
                    sql3 = f"UPDATE posts SET verified = 't' WHERE rowid = {id_post}"
                    insert(sql3, ())
                count_post += 1
    except Exception as ex:
        print(ex)
    finally:
        sql_null = f"UPDATE posts SET verified = 't' WHERE text = ''"
        insert(sql_null, ())
        print(f'Формирование списка постов для отправки закончен.\nСформированно {count_post} постов.\n Время:{datetime.now()}')


def start_schedule():
    schedule.every().day.at("09:00").do(generate_list_to_send)

    schedule.every().day.at("14:00").do(generate_list_to_send)

    schedule.every().day.at("21:30").do(generate_list_to_send)

    while True:
        schedule.run_pending()
        time.sleep(30)
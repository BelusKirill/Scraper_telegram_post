import sqlite3

from datetime import datetime
from tzlocal import get_localzone

tz = get_localzone()

def get_data_line(sql: str) -> list:
    record: list = None
    try:
        sqliteConnection = sqlite3.connect('db/database.sqlite')
        cursor = sqliteConnection.cursor()
        #print("Сосданно соединение с SQLite")

        cursor.execute(sql)
        record = cursor.fetchall()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #print("SQLite соединение закрыто")
        if record != None and len(record) > 0:
            return record[0]
        else:
            return None


def get_data(sql: str) -> list:
    record: list = None
    try:
        sqliteConnection = sqlite3.connect('db/database.sqlite')
        cursor = sqliteConnection.cursor()

        cursor.execute(sql)
        record = cursor.fetchall()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        if record != None and len(record) > 0:
            return record
        else:
            return None


def insert(sql: str):
    try:
        sqliteConnection = sqlite3.connect('db/database.sqlite')
        cursor = sqliteConnection.cursor()

        cursor.execute(sql)
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def insert(sql: str, params):
    try:
        sqliteConnection = sqlite3.connect('db/database.sqlite')
        cursor = sqliteConnection.cursor()

        cursor.execute(sql, params)
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def insert_get_id(sql: str):
    record = None
    try:
        sqliteConnection = sqlite3.connect('db/database.sqlite')
        cursor = sqliteConnection.cursor()

        cursor.execute(sql)
        sqliteConnection.commit()

        cursor.execute("SELECT last_insert_rowid()")
        record = cursor.fetchall()

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        if record != None and len(record) > 0:
            return record[0][0]
        else:
            return None


def insert_posts(array: list, name_channel: str):
    try:
        sqliteConnection = sqlite3.connect('db/database.sqlite')
        cursor = sqliteConnection.cursor()
        print("Сосданно соединение с SQLite")

        for line in array:
            sql = "INSERT INTO posts (channel, photos, text, date, verified) \
                    VALUES (?, ?, ?, ?, 'f')"
            cursor.execute(sql, (name_channel, None, line['message'], line['date'].astimezone(tz), ))
            sqliteConnection.commit()

        sql = f"UPDATE history_appeals \
        SET date='{datetime.now().astimezone(tz)}' \
        WHERE channel='{name_channel}';"
        cursor.execute(sql)

        sql = f"INSERT INTO history_appeals (channel, date) \
        SELECT '{name_channel}', '{datetime.now().astimezone(tz)}' \
        WHERE (Select Changes() = 0);"
        cursor.execute(sql)

        sqliteConnection.commit()

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("SQLite соединение закрыто")



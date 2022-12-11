import sqlite3

def get_data_line(sql: str) -> list:
    record: list = None
    try:
        sqliteConnection = sqlite3.connect('db/database.sqlite')
        cursor = sqliteConnection.cursor()
        print("Сосданно соединение с SQLite")

        cursor.execute(sql)
        record = cursor.fetchall()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        if record != None and len(record) > 0:
            return record[0]
        else:
            return None


def get_data(sql: str) -> list:
    record: list = None
    try:
        sqliteConnection = sqlite3.connect('db/database.sqlite')
        cursor = sqliteConnection.cursor()
        print("Сосданно соединение с SQLite")

        cursor.execute(sql)
        record = cursor.fetchall()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        if record != None and len(record) > 0:
            return record
        else:
            return None


def insert(sql: str):
    try:
        sqliteConnection = sqlite3.connect('db/database.sqlite')
        cursor = sqliteConnection.cursor()
        print("Сосданно соединение с SQLite")

        cursor.execute(sql)
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
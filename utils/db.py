import datetime
import sqlite3
from contextlib import closing
from sqlite3 import Connection, Cursor
from utils import sheets

database = "utils/database.db"


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def start():
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users(user_id INT, username TEXT, first_name TEXT, fio TEXT, is_active BOOL)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS records(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INT, arrival_date TEXT, arrival_time TEXT, arrival_location TEXT, leaving_date TEXT, leaving_time TEXT, leaving_location TEXT, note TEXT)")
        connection.commit()


def get_user(user_id):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("SELECT is_active FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone()


def add_user(user_id, username, first_name, fio):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, FALSE)", (user_id, username, first_name, fio))
        connection.commit()


def activate_user(user_id):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("UPDATE users SET is_active = TRUE WHERE user_id = ?", (user_id,))
        connection.commit()


def delete_user(user_id):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        connection.commit()


def add_arrival(user_id, location):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        today = datetime.datetime.now()
        cursor.execute("INSERT INTO records(user_id, arrival_date, arrival_time, arrival_location) VALUES (?, ?, ?, ?)",
                       (user_id, today.strftime("%d.%m.%Y"), today.strftime("%H:%M"), location))
        connection.commit()


def add_leaving(user_id, record_data):
    with closing(sqlite3.connect(database)) as connection:
        cursor: Cursor = connection.cursor()
        today = datetime.datetime.now()
        cursor.execute(
            "UPDATE records SET leaving_date = ?, leaving_time = ?, leaving_location = ?, note = ? WHERE user_id = ? and arrival_date = ?",
            (
                today.strftime("%d.%m.%Y"), today.strftime("%H:%M"), record_data["location"], record_data["note"],
                user_id, today.strftime("%d.%m.%Y")))
        connection.commit()

        cursor.execute(
            "SELECT users.fio, arrival_date, arrival_time, arrival_location, leaving_date, leaving_time, leaving_location, note FROM records JOIN users ON users.user_id = records.user_id WHERE records.user_id = ? and arrival_date = ?",
            (user_id, today.strftime("%d.%m.%Y")))

        record_data = list(cursor.fetchone())
        record_data.insert(0, "")
        sheets.append_record(record_data)


def get_arrival(user_id):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        today = datetime.datetime.now()
        cursor.execute("SELECT id FROM records WHERE user_id = ? and arrival_date = ?",
                       (user_id, today.strftime("%d.%m.%Y")))
        return cursor.fetchone()


def get_leaving(user_id):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        today = datetime.datetime.now()
        cursor.execute("SELECT id FROM records WHERE user_id = ? and leaving_date = ?",
                       (user_id, today.strftime("%d.%m.%Y")))
        return cursor.fetchone()

from django.conf import settings
import sqlite3


def connect():
    conn = sqlite3.connect(settings.SQLITE3_FILE)
    c = conn.cursor()
    return conn, c



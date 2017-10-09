import sqlite3


def connect():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    return conn, c


def directory(path):
    p = path.decode('utf-8')
    w = p.split('/')[:-1]
    image_path = '/'.join(w)
    return image_path


def dirname(file):
    return '/'.join(file.split('/')[:-2])


def filename(file):
    return file.split('/')[-1]



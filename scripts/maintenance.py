from __future__ import unicode_literals

import sqlite3

from flac.db import delete_album_completely

db_path = '../../db.sqlite3'


def delete_albums(ids):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    for aid in ids:
        delete_album_completely(aid, c, conn)
        print('removed id:{}'.format(aid))


def main():
    delete_albums([5087, 5086, 5088, ])


if __name__ == '__main__':
    main()

from __future__ import unicode_literals
# encoding: utf-8
# coding=utf-8
import os
import sqlite3
from venv.flac.db import (get_album_id_by_path, )
from venv.flac.scripts.flacs import skipdirs

'''
check how far we are, putting 'albums' in the database
when looking at certain  directories
'''

db_path = '../../db.sqlite3'


def output_file(fname, lines):
    s = ''
    for line in lines:
        s += line + '\n'
    with open(fname, b"w") as fp:
        fp.write(s.encode('utf-8'))


def process(p, c, conn, lines, present):
    album = get_album_id_by_path(p, c, conn)
    if not album:
        lines.append(p)
    else:
        present.append(p)


def main():
    path = "/Volumes/Media/Audio/Klassiek/Performers"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    lines = []
    present = []
    for d in os.listdir(path):
        p = u'{}/{}'.format(path, d)
        if os.path.isdir(p) and d not in skipdirs:
            process(p, c, conn, lines, present)
    output_file('check.txt', lines)
    output_file('present.txt', present)


if __name__ == '__main__':
    main()

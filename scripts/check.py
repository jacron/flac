from __future__ import unicode_literals

import glob
import os
import sqlite3

from venv.flac.scripts.helper.insert import play_types
from venv.flac.db import (get_album_id_by_path, )
from venv.flac.scripts.flacs import skipdirs

'''
check how far we are, putting 'albums' in the database
when looking at certain  directories
'''

db_path = '../../db.sqlite3'
path = "/Volumes/Media/Audio/Klassiek/Componisten"


def output_file(fname, lines):
    s = ''
    for line in lines:
        s += line + '\n'
    with open(fname, b"w") as fp:
        fp.write(s.encode('utf-8'))


def process(p, c, conn, lines, present):
    count = 0
    for card in play_types:
        files_path = u"{}{}".format(p, "/*.{}".format(card))
        for f in glob.iglob(files_path):
            count += 1
    if count == 0:
        return
    album = get_album_id_by_path(p, c, conn)
    if not album:
        lines.append(p)
    else:
        present.append(p)


def main():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    lines = []
    present = []
    count = 0
    for d in os.listdir(path):
        p = '{}/{}'.format(path, d)
        if os.path.isdir(p) and d not in skipdirs:
            for d2 in os.listdir(p):
                p2 = '{}/{}'.format(p, d2)
                if os.path.isdir(p2) and d2 not in skipdirs:
                    print(d2)
                    count += 1
                    process(p2, c, conn, lines, present)
    output_file('check.txt', lines)
    output_file('present.txt', present)
    print('processed: {}'.format(count))


if __name__ == '__main__':
    main()

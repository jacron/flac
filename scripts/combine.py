"""flac

"""
import glob
import sqlite3
# importing for stand alone script
from venv.flac.services import dirname, filename

cuesheet_extension = '.cue'
flac_wild = "/*.flac"

combine_path = "/Volumes/Media/Audio/Klassiek/Componisten/Scarlatti, D/sonaten clavecimbel/Sonatas - Belder/"
combine_part = ["Disc 1of3", "Disc 2of3", "Disc 3of3", ]


def script_connect():
    # let op: het pad naar de database moet relatief zijn, omdat dit script stand alone uitgevoerd wordt!
    conn = sqlite3.connect('../../db.sqlite3')
    c = conn.cursor()
    return conn, c


def combine_file(filepath, nr):
    target = dirname(filepath) + '/' + nr + filename(filepath)
    print(filepath)
    print(target)
    # os.rename(file, target)


def combine():
    for album in combine_part:
        nr = album.split()[1][0]
        p = combine_path + album + flac_wild
        print(p)
        [combine_file(f, nr) for f in glob.iglob(p)]


def main():
    combine()

if __name__ == '__main__':
    main()

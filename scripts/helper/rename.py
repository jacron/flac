import glob
from shutil import copyfile

from flac.db import set_album_title, get_album_by_path
from venv.flac.services import (
    has_haakjes, replace_haakjes, get_full_cuesheet)
import os

cover_names = ['box front', 'front', 'Cover', 'cover', 'Front']
cover_nice = 'folder.jpg'
back_names = ['Back.jpg']
back_nice = 'back.jpg'


def rename_cover_one(path, name):
    src = u'{}/{}.jpg'.format(path, name)
    # print(src)
    if os.path.exists(src):
        # print(src)
        trg = u'{}/{}'.format(path, cover_nice)
        if not os.path.exists(trg):
            os.rename(src, trg)
            print('renamed to:{}'.format(trg))


def rename_cover(path, step_in):
    for name in cover_names:
        rename_cover_one(path, name)
        if step_in:
            # one recursive step
            for d2 in os.listdir(path):
                p2 = u'{}/{}'.format(path, d2)
                if os.path.isdir(p2):
                    rename_cover_one(p2, name)


def rename_back_one(path, name):
    src = '{}/{}.jpg'.format(path, name)
    if os.path.exists(src):
        trg = '{}/{}'.format(path, back_nice)
        if not os.path.exists(trg):
            os.rename(src, trg)
            print('renamed to:{}'.format(trg))


def rename_back(path, step_in):
    for name in back_names:
        rename_back_one(path, name)
        if step_in:
            # one recursive step
            for d2 in os.listdir(path):
                p2 = u'{}/{}'.format(path, d2)
                if os.path.isdir(p2):
                    rename_back_one(p2, name)


def rename_to_back_one(path):
    jpgpath = u'{}/scan/Booklet*.jpg'.format(path)
    for src in glob.iglob(jpgpath):
        trg = '{}/back.jpg'.format(path)
        if not os.path.exists(trg):
            copyfile(src, trg)
            print(src)
            print('copied to:{}'.format(trg))


def rename_to_back(path):
    for d2 in os.listdir(path):
        p2 = u'{}/{}'.format(path, d2)
        if os.path.isdir(p2):
            rename_to_back_one(p2)


def restore_cover_one(path, fro, to):
    src = u'{}/{}.jpg'.format(path, fro)
    # print(src)
    if os.path.exists(src):
        trg = u'{}/{}.jpg'.format(path, to)
        # print(trg)
        if os.path.exists(trg):
            os.unlink(trg)
            os.rename(src, trg)
            print(u'renamed to:{}'.format(trg))


def restore_cover(path, step_in):
    """
    herstel covers, waar .big varianten bestaan

    :param path:
    :param step_in:
    :return:
    """
    restore_cover_one(path, 'back.big', 'back')
    restore_cover_one(path, 'folder.big', 'folder')
    if step_in:
        for d2 in os.listdir(path):
            p2 = u'{}/{}'.format(path, d2)
            # print(p2)
            if os.path.isdir(p2):
                restore_cover_one(p2, 'back.big', 'back')
                restore_cover_one(p2, 'folder.big', 'folder')


def sanatize_haakjes_one(path, d):
    src = u'{}/{}'.format(path, d)
    if os.path.exists(src) and os.path.isdir(src):
        if has_haakjes(d):
            d_trg = replace_haakjes(d)
            dst = u'{}/{}'.format(path, d_trg)
            os.rename(src, dst)
            print(dst)
            return dst
        else:
            return src
    return None


def sanatize_haakjes(path, step_in):
    for d in os.listdir(path):
        dst = sanatize_haakjes_one(path, d)
        if dst and step_in:
            # one recursive step
            for d2 in os.listdir(dst):
                p2 = u'{}/{}'.format(dst, d2)
                sanatize_haakjes_one(p2, d2)


def album_by_path(p, c, conn):
    return get_album_by_path(p, c, conn)


def rename_all_titles(path, skipdirs, c, conn):
    for d in os.listdir(path):
        p = u'{}/{}'.format(path, d)
        if os.path.isdir(p) and d not in skipdirs:
            nr = u'{}{}'.format(d[-2],d[-1])
            # if int(nr) > 0:
            cuepath = u'{}/lijst.cue'.format(p)
            if not os.path.exists(cuepath):
                cuepath = u'{}/*.cue'.format(p)
                for ncue in glob.iglob(cuepath):
                    cuepath = ncue
                    # return
            cue = get_full_cuesheet(cuepath, 0)
            # full_title = '{} - {}'.format(nr, cue['Title'])
            full_title = '{}'.format(cue['Title'])
            print(full_title)

            album = album_by_path(p, c, conn)
            print(album['Title'])
            set_album_title(album['ID'], full_title, c, conn)



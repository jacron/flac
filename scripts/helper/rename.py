from venv.flac.services import (
    has_haakjes, replace_haakjes,)
import os

cover_names = ['box front', 'front', 'Cover', 'cover']
cover_nice = 'folder.jpg'


def rename_cover_one(path, name):
    src = '{}/{}.jpg'.format(path, name)
    if os.path.exists(src):
        trg = '{}/{}'.format(path, cover_nice)
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
                    rename_cover_one(p2, d2)


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
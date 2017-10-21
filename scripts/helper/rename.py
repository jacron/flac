from venv.flac.services import(
    has_haakjes, replace_haakjes,)
import os
import glob

cover_names = ['box front', 'front', 'Cover', 'cover']
cover_nice = 'folder.jpg'


def rename_cover(path):
    for name in cover_names:
        src = '{}/{}.jpg'.format(path, name)
        trg = '{}/{}'.format(path, cover_nice)
        if os.path.exists(trg):
            return
        if os.path.exists(src):
            os.rename(src, trg)
            print('renamed to:{}'.format(trg))


def sanatize_haakjes(path, d):
    # print(d)
    if has_haakjes(d):
        src = '{}/{}'.format(path, d)
        dst = '{}/{}'.format(path, replace_haakjes(d))
        if os.path.exists(src):
            os.rename(src, dst)
            print(dst)


# def process_path(path, f):
#     print(f)
#     p = '{}/{}'.format(path, f)
#     if os.path.isdir(p):
#         for ff in os.listdir(p):
#             print(ff)
#             src = u'{}/{}'.format(p, ff)
#             trg = u'{}/{}'.format(os.path.dirname(p), ff)
#             print(src)
#             print(trg)
#             print('--')
#             # os.rename(p, trg)



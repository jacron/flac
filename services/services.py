import os
from flac.settings import COMPONIST_PATH, PERFORMER_PATH, COVER_PATH, TMP_PATH
from PIL import ImageGrab


def replace_haakjes(s):
    for ch in ['[', '{']:
        if ch in s:
            s = s.replace(ch, '(')
    for ch in [']', '}']:
        if ch in s:
            s = s.replace(ch, ')')
    return s


def has_haakjes(s):
    # print(s)
    for ch in ['[', '{']:
        if ch in s:
            return True
    for ch in [']', '}']:
        if ch in s:
            return True
    return False


def directory(path):
    # path = path.decode('utf-8')
    w = path.split('/')[:-1]
    image_path = '/'.join(w)
    return image_path


def dirname(ffile):
    return '/'.join(ffile.split('/')[:-2])


def filename(ffile):
    return ffile.split('/')[-1]


def trimextension(ffile):
    ff = ffile.split('.')[:-1]
    return '.'.join(ff)


def dequote(line):
    line = line.strip()
    if line.startswith('"'):
        line = line[1:]
    if line.endswith('"'):
        line = line[:-1]
    return line


def splits_comma_naam(naam):
    c_namen = naam.split(',')
    if len(c_namen) > 1:
        c_firstname = c_namen[1].strip()
        c_lastname = c_namen[0].strip()
    else:
        c_firstname = ''
        c_lastname = naam.strip()
    return c_firstname, c_lastname


def splits_naam(naam):
    if len(naam.split(',')) > 1:
        return splits_comma_naam(naam)
    c_namen = naam.split()
    if len(c_namen) > 1:
        c_lastname = c_namen[-1].strip()
        c_firstname = ' '.join(c_namen[:-1]).strip()
    else:
        c_firstname = ''
        c_lastname = naam.strip()
    return c_firstname, c_lastname


def splits_years(years):
    c_years = years.split('-')
    if len(c_years) < 2:
        return years.strip(), ''
    return c_years[0].strip(), c_years[1].strip()


def syspath_componist(componist):
    path = u'{}{}'.format(COMPONIST_PATH, componist['LastName'])
    return path


def syspath_performer(performer):
    name = performer['FullName']
    path = u'{}{}'.format(PERFORMER_PATH, name)
    return path


def alfabet():
    return [chr(i) for i in range(ord('a'),ord('z')+1)]


def save_cb_image(cover):
    img = ImageGrab.grabclipboard()
    if img:
        img.save(COVER_PATH.format(cover))
        openpath(TMP_PATH)


def openpath(path):
    cmd = u'open "{}"'.format(path).encode('UTF-8')
    os.system(cmd)



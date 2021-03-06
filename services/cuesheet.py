# from __future__ import unicode_literals
import codecs


from .services import dequote
import os


class Error(Exception):
    pass


class NotFoundError(Error):
    pass


def get_title(data):
    for line in data.split('\n'):
        line = line.strip()
        pos = line.find('TITLE ')
        if pos != -1:
            rest = pos + len('TITLE ')
            line = line[rest:-1]
            return dequote(line)


def get_element(line, prefix):
    pos = line.find(prefix)
    if pos != -1:
        rest = pos + len(prefix)
        result = line[rest:]
        return result
    return None


def replace_haakjes(s):
    for ch in ['[', '{']:
        if ch in s:
            s = s.replace(ch, '(')
    for ch in [']', '}']:
        if ch in s:
            s = s.replace(ch, ')')
    return s


def parse(data):
    cue = {
        'title': None,
        'performer': None,
        'files': [],
        'rem': [],
    }
    cfile = None
    ctrack = None
    for line in data.split(b'\n'):
        # try:
        #     line = unidecode(line)
        # except Exception:
        #     pass
        if len(line) < 1:
            continue

        rem = get_element(line, 'REM ')
        if rem:
            cue['rem'].append(rem)

        title = get_element(line, 'TITLE ')
        if title:
            if ctrack:
                # try:
                #     ctrack['title'] = unidecode(replace_haakjes(dequote(title)))
                # except Exception:
                ctrack['title'] = replace_haakjes(dequote(title))
            else:
                cue['title'] = dequote(title)

        performer = get_element(line, 'PERFORMER ')
        if performer:
            if ctrack:
                ctrack['performer'] = dequote(performer)
            else:
                cue['performer'] = dequote(performer)

        efile = get_element(line, 'FILE ')
        if efile:
            if cfile:
                cue['files'].append(cfile)
            name = ' '.join(efile.split()[:-1])
            cfile = {
                'name': dequote(name),
                'tracks': [],
            }

        track = get_element(line, 'TRACK ')
        if track:
            nr, name = track.split()
            if ctrack:
                cfile['tracks'].append(ctrack)
            ctrack = {
                'nr': nr,
                'name': name,
            }

        index = get_element(line, 'INDEX ')
        if index:
            nr, time = index.split()
            if ctrack:
                ctrack['index'] = {
                    'nr': nr,
                    'time': time,
                }
    if ctrack:
        cfile['tracks'].append(ctrack)
    if cfile:
        cue['files'].append(cfile)
    return cue


def get_full_cuesheet(path, id):
    filename = os.path.split(path)[1]
    filename = ' '.join(filename.split('.')[:-1])
    path = path.encode('utf-8')
    if os.path.exists(path):
        with codecs.open(path, b'r', 'utf-8') as f:
            try:
                data = f.read()
            except:
                print("can't read unicode here")
                with open(path, b'r') as f:
                    data = f.read()
            cue = None
            try:
                cue = parse(data)
            except:
                print('parse cue failed')
            return {
                'Filename': filename,
                'Title': cue['title'],
                'ID': id,
                'cue': cue,
            }
    else:
        raise NotFoundError

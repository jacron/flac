from .services import dequote
import os


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
        return line[rest:]
    return None


def display(cue):
    # lines = [cue['title'], cue['performer']]
    lines = []
    for rem in cue['rem']:
        lines.append(rem)
    for file in cue['files']:
        lines.append(file['name'])
        for track in file['tracks']:
            # lines.append('  {} {}'.format(track['nr'], track['name']))
            lines.append('- {}'.format(track['title']))
    return lines


def parse(data):
    cue = {
        'title': None,
        'performer': None,
        'files': [],
        'rem': [],
    }
    cfile = None
    ctrack = None
    for line in data.split('\n'):
        line = line.strip()

        # rem = get_element(line, 'REM ')
        # if rem:
        #     cue['rem'].append(rem)

        title = get_element(line, 'TITLE ')
        if title:
            if ctrack:
                ctrack['title'] = dequote(title)
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

    # show(cue)
    print(cue)
    # print(display(cue))
    return cue


def get_full_cuesheet(path, id):
    filename = os.path.split(path)[1]
    filename = ' '.join(filename.split('.')[:-1])
    with open(path, 'r') as f:
        data = f.read()
        return {
            'Title': filename,
            'ID': id,
            'cuesheet': display(parse(data)),
        }


def get_cuesheet(filename, id):
    filename = ' '.join(filename.split('.')[:-1])
    return {
        'Title': filename,
        'ID': id,
    }

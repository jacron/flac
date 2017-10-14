from .services import dequote


def get_title(data):
    for line in data.split('\n'):
        line = line.strip()
        pos = line.find('TITLE ')
        if pos != -1:
            rest = pos + len('TITLE ')
            line = line[rest:-1]
            return dequote(line)


def get_cuesheet_title(path, id):
    with open(path, 'r') as f:
        data = f.read()
        return {
            'Title': get_title(data),
            'ID': id,
        }


def get_cuesheet(filename, id):
    filename = ' '.join(filename.split('.')[:-1])
    return {
        'Title': filename,
        'ID': id,
    }

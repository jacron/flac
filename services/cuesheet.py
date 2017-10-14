from .services import dequote


def get_title(data):
    for line in data.split('\n'):
        line = line.strip()
        pos = line.find('TITLE ')
        if pos != -1:
            rest = pos + len('TITLE ')
            line = line[rest:-1]
            return dequote(line)


def get_cuesheet(path, id):
    with open(path, 'r') as f:
        data = f.read()
        return {
            'Title': get_title(data),
            'ID': id
        }



def directory(path):
    # path = path.decode('utf-8')
    w = path.split('/')[:-1]
    image_path = '/'.join(w)
    return image_path


def dirname(file):
    return '/'.join(file.split('/')[:-2])


def filename(file):
    return file.split('/')[-1]


def splits_comma_naam(naam):
    c_namen = naam.split(',')
    if len(c_namen) > 1:
        c_firstname = c_namen[1]
        c_lastname = c_namen[0]
    else:
        c_firstname = ''
        c_lastname = naam
    return c_firstname, c_lastname


def splits_naam(naam):
    if len(naam.split(',')) > 1:
        return splits_comma_naam(naam)
    c_namen = naam.split()
    if len(c_namen) > 1:
        c_firstname = c_namen[0]
        c_lastname = c_namen[1]
    else:
        c_firstname = ''
        c_lastname = naam
    return c_firstname, c_lastname


def menu_items():
    return [
            {'href': '/home',
             'label': 'Home',
             },
            {'href': '/componist',
             'label': 'Componist',
             },
            {'href': '/performer',
             'label': 'Artiest',
             },
            {'href': '/instrument',
             'label': 'Instrument',
             },
            {'href': '/album',
             'label': 'Album',
             },
        ]
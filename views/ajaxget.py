import json

from ..db import (
    get_tags,
    get_componisten_typeahead, get_performers_typeahead, get_instruments_typeahead,
    get_general_search, get_album_by_path, connect)


def do_get(get):
    cmd = get['cmd']
    if cmd == 'tags':
        return json.dumps(get_tags())
    if cmd == 'componisten':
        return json.dumps(get_componisten_typeahead())
    if cmd == 'performers':
        return json.dumps(get_performers_typeahead())
    if cmd == 'instruments':
        return json.dumps(get_instruments_typeahead())
    if cmd == 'generalsearch':
        return json.dumps(get_general_search(get['query']))
    if cmd == 'album_by_path':
        conn, c = connect()
        return json.dumps(get_album_by_path(get['path'], c))
    return 'unknown cmd'

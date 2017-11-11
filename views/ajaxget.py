import json

from ..db import (
    get_tags,
    get_componisten_typeahead, get_performers_typeahead, get_instruments_typeahead,
)


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
    return 'unknown cmd'

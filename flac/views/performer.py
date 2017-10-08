import sqlite3

from django.http import HttpResponse
from django.template import loader


def connect():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    return conn, c


def performer(request, id):
    conn, c = connect()
    template = loader.get_template('flac/performer.html')
    sql = '''
      SELECT FirstName, LastName, ID from Performer
    '''
    items = [item for item in c.execute(sql).fetchall()]
    conn.close()
    context = {
        'items': items,
    }
    return HttpResponse(template.render(context, request))


import sqlite3

from django.http import HttpResponse
from django.template import loader


def connect():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    return conn, c


def instrument(request, id):
    conn, c = connect()
    template = loader.get_template('flac/album.html')

    sql = '''
      SELECT Name, ID from Instrument WHERE ID=?
    '''
    name = c.execute(sql, id).fetchone()

    sql = '''
      SELECT Title, ID from Album 
      WHERE InstrumentID=?
      ORDER BY Title
    '''
    items = [item for item in c.execute(sql, id).fetchall()]
    conn.close()

    context = {
        'items': items,
        'instrument': name,
    }
    return HttpResponse(template.render(context, request))

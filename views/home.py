import sqlite3

from django.http import HttpResponse
from django.template import loader


def connect():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    return conn, c


def home(request):
    conn, c = connect()
    template = loader.get_template('flac/home.html')
    sql = '''
      SELECT Title, ID from Album
    '''
    items = [item for item in c.execute(sql).fetchall()]
    conn.close()
    return HttpResponse(template.render({'items': items,}, request))

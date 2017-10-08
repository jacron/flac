import sqlite3
import time
from django.http import HttpResponse
from django.template import loader
from . import flacs

def connect():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    return conn, c


def now():
    return time.strftime("%d/%m/%Y - %H:%M:%S")


def home(request):
    conn, c = connect()
    template = loader.get_template('home.html')
    sql = '''
    SELECT Title, ID from Album
    '''
    items = [item for item in c.execute(sql).fetchall()]
    conn.close()

    context = {
        'items': items,
        'now': now()
    }
    return HttpResponse(template.render(context, request))


def album(request, id):
    conn, c = connect()
    template = loader.get_template('album.html')
    sql = '''
    SELECT Name, ID from Piece WHERE AlbumID=?
    '''
    items = [item for item in c.execute(sql, id).fetchall()]
    conn.close()
    context = {
        'items': items,
        'now': now()
    }
    return HttpResponse(template.render(context, request))


def performer(request, id):
    conn, c = connect()
    template = loader.get_template('performer.html')
    sql = '''
    SELECT FirstName, LastName, ID from Performer
    '''
    items = [item for item in c.execute(sql).fetchall()]
    conn.close()
    context = {
        'items': items,
        'now': now()
    }
    return HttpResponse(template.render(context, request))


def piece(request, id):
    conn, c = connect()
    template = loader.get_template('piece.html')
    sql = '''
    SELECT Name, File, ID from Piece
    '''
    items = [item for item in c.execute(sql).fetchall()]
    conn.close()
    context = {
        'items': items,
        'now': now()
    }
    return HttpResponse(template.render(context, request))

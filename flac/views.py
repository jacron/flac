import sqlite3
from django.http import HttpResponse
from django.template import loader
from . import flacs

def home(request):
    # flacs.main()
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    sql = '''
    SELECT Name from Piece
    '''
    pieces = [piece[0] for piece in c.execute(sql).fetchall()]
    template = loader.get_template('home.html')

    context = {
        'pieces': pieces
    }
    # html = '<table>'
    # for piece in pieces:
    #     html += '<tr><td>' + piece[0] + '</td></tr>'
    return HttpResponse(template.render(context, request))
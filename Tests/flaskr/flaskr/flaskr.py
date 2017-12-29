import os, sqlite3

from flask import (Flask, request, session, g, redirect, url_for, \
abort, render_template, flash)

app = Flask(__name__) # create application
app.config.from_object(__name__) # load config from this file, flaskr.py

app.config.update(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY=b'\xaf\xbeE\xcb\xfa\x91\x99\x03\x12J\x1aj36\x84\xc8',
    USERNAME='admin',
    PASSWORD='default'
)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to a specific database"""

    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite.db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite.db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()

    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())

    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database"""
    init_db()
    print('Initialized the database.')

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

from flask import Flask, render_template, url_for, g
import sqlite3
import os


DATABASE = '/tmp/site.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
app.config.from_object(__name__)


app.config.update(dict(
  DATABASE=os.path.join(app.root_path, 'site.db'),
  DEBUG=True,
  SECRET_KEY='development key',
  USERNAME='admin',
  PASSWORD='default'
  ))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
  rv = sqlite3.connect(app.config['DATABASE'])
  rv.row_factory = sqlite3.Row
  return rv

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
    db.commit()



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add/')
def add():
    return None

if __name__ == '__main__':
    app.run(use_reloader=False) # type: ignore
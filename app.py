from flask import *
import sqlite3 as sqlite
import os

app = Flask(__name__)

app.config.update(
    DATABASE = os.path.join(app.root_path, 'database.db'),
    DEBUG=True,
    USERNAME='admin',
    PASSWORD='123',
    SECRET_KEY='kjhfasT^&^(#RG)'
)


def connect_db():
    conn = sqlite.connect(app.config['DATABASE'])
    conn.row_factory = sqlite.Row
    return conn

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('tplate.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()







@app.route('/', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash("You're logged in")
            return redirect(url_for('show_db'))
        
    return render_template('login.html', error = error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("You're logout")
    return redirect(url_for('login'))

@app.route('/database')
def show_db():
    if session['logged_in'] != True:
        abort(401)
    
    with get_db() as db:
        cur = db.execute('SELECT * from corp order by id desc')
        db = cur.fetchall()

    return render_template('show_db.html', entries = db)

@app.route('/add', methods = ['POST'])
def add():
    if session['logged_in'] != True:
        abort(401)

    with get_db() as db:
        db.execute('insert into corp (corporation, city) values (?, ?)', [request.form['corporation'], request.form['city']])
        db.commit()

    flash('New entry was successfully posted')

    return redirect(url_for('show_db'))

if __name__ == '__main__':
    app.run()
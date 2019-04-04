from collections import defaultdict
from functools import wraps

import pymysql
from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   session, url_for)
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash

mysql = MySQL()

app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = 'cowabunga'

app.config['MYSQL_DATABASE_USER'] = "MeanderingArma"
app.config['MYSQL_DATABASE_PASSWORD'] = "Dillos1999"
app.config['MYSQL_DATABASE_DB'] = "YCS"
app.config['MYSQL_DATABASE_HOST'] = "yuppie-city-simulator-db.cohu57vlr7rd.us-east-2.rds.amazonaws.com"
mysql.init_app(app)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first!')
            redirect(url_for('home'))

    return wrap


test_db = defaultdict(lambda: '')
test_db['username'] = 'test'
test_db['password'] = 'testword'
test_db['email'] = 'test@email.com'


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/data')
def data():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM city_index")
        rows = cursor.fetchall()
        for row in rows:
            print(row['city_name'])
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return render_template("data.html", data=rows)


@app.route('/quiz')
def quiz():
    return render_template("quiz.html")


@app.route('/user')
@login_required
def user():
    return render_template("user.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == test_db['email'] and password == test_db['password']:
            session['logged_in'] = True
            flash('Login successful')
            return redirect(url_for('home'))

        else:
            error = 'Invalid credentials! Please try again.'
            flash('Invalid credentials')

    return render_template('index.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('Logout successful')
    return redirect(url_for('home'))


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        test_db[request.form['username']] = request.form['password']
        test_db[request.form['email']] = request.form['password']

    return render_template('index.html')


@app.route('/test')
def test():
    return render_template('test.html')


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == "__main__":
    app.run()

from collections import defaultdict
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash
import pymysql
from flask import Flask, jsonify, request, render_template, session, redirect, url_for, flash, json
from functools import wraps

from src.helper_classes.quiz_results import QuizResults
from src.algorithm.algorithm import AlgorithmRunner
from src.controller.Controller import Controller

import webbrowser

mysql = MySQL()
controller = Controller()

app = Flask(__name__)
app.config["DEBUG"] = False
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
            return redirect(url_for('home'))

    return wrap


test_db = defaultdict(lambda: '')

test_db['user_id'] = '10000'
test_db['username'] = 'Yeezy'
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
        cursor.execute("SELECT * FROM city_index_raw")
        rows = cursor.fetchall()
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
            session['email'] = email
            session['name'] = "Test"
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


@app.route('/quizResults', methods=['GET', 'POST'])
def quiz_results():
    if request.method == 'POST':
        # Convert user input from request object into a dictionary that will drive a QuizResults object
        values_as_string_dict = request.form.to_dict()
        values_as_int_dict = {}
        for key, value in values_as_string_dict.items():
            values_as_int_dict[key] = 0 if value == "" else int(value)

        top_city_object_list, city_scores_dict = controller.run_quiz_workflow(
            values_as_int_dict)

        return render_template('view_results.html', scores=city_scores_dict, data=top_city_object_list)


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
    webbrowser.get().open("http://127.0.0.1:5000/")
    app.run(host='127.0.0.1')

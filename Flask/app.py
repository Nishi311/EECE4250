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
test_db['user_id'] = '10000'
test_db['username'] = 'Yeezy'
test_db['password'] = 'testword'
test_db['email'] = 'test@email.com'


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/data')
def data():
    return render_template("data.html")


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


@app.route('/quizResults', methods=['GET', 'POST'])
def quiz_results():
    if request.method == 'POST':
        weight_list = []
        attribute_list = "walkability, " + "bikeability, " + "transit, " + "traffic, " + "metro_pop, " + \
            "pop_density, " + "prop_crime, " + \
            "violent_crime, " + "air_pollution, " + "sunshine"
        attribute_list = attribute_list.split(", ")
        print(attribute_list)
        for factor in attribute_list:
            weight_list.append(request.form[factor])
        print(weight_list)

        if len(attribute_list) == len(weight_list):
            combined_dict = {}

            for index in range(len(attribute_list)):
                combined_dict[attribute_list[index]
                              ] = float(weight_list[index])

            raw_quiz_results = QuizResults(combined_dict)

            algo_runner = AlgorithmRunner()
            processed_quiz_results = algo_runner.run_module(raw_quiz_results)
            # TODO: Ask nick about how to get the actual user ID
            # controller.store_new_quiz(99999, processed_quiz_results)

            city_scores_dict = defaultdict()
            city_names = []
            for city_tuple in processed_quiz_results.return_city_scores():
                city_scores_dict[city_tuple[0]] = int(city_tuple[1])
                city_names.append(city_tuple[0])

            print(city_names)

            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM city_index WHERE city_name IN ('{0}','{1}','{2}','{3}','{4}')".format(
                city_names[0], city_names[1], city_names[2], city_names[3], city_names[4]))
            rows = cursor.fetchall()
            print(rows)

        return render_template('view_results.html', scores=city_scores_dict, data=rows)


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


class BasicLauncher(object):
    @staticmethod
    def run_module():
        webbrowser.get('windows-default').open("http://127.0.0.1:5000/")
        app.run(host='127.0.0.1')

# if __name__ == "__main__":
#     webbrowser.get('windows-default').open("http://127.0.0.1:5000/")
#     app.run(host='127.0.0.1')

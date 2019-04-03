from collections import defaultdict
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash
import pymysql
from flask import Flask, jsonify, request, render_template, session, redirect, url_for, flash
from functools import wraps

app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = 'cowabunga'

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

@app.route('/create', methods = ['GET', 'POST'])
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

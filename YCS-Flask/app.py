import pymysql
from flask import Flask, jsonify, request, render_template, session, send_from_directory, send_file
from werkzeug.security import generate_password_hash
from flaskext.mysql import MySQL
from collections import defaultdict

app = Flask(__name__)
app.config["DEBUG"] = True
# app.add_url_rule('/templates/<path:filename>', endpoint='templates',
#                  view_func=app.send_file)

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
def user():
    return render_template("user.html")

@app.route('/login')
def login():
    try:
        json = request.json
        username = json['username']
        password = json['password']
        email = json['email']
        
        # validate the received values
        if ((username and password) or (email and password)):
            # validate credentials
            if username == test_db['username'] and password == test_db['password']:
                resp = jsonify('Login successful!')
                resp.status_code = 200
                return resp
        else:
            return not_found()
    except Exception as e:
        print(e)

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

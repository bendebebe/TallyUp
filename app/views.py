import os
from flask import render_template, Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

with app.test_request_context('/index', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    assert request.path == '/index'
    assert request.method == 'POST'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['POST','GET'])
def register():
    return render_template('register.html', title='Register')

@app.route('/login', methods=['POST','GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', title='Sign In', error=error)

if __name__ == '__main__':
    app.run()

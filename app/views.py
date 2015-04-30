import os
from flask import render_template, Flask, url_for, redirect, request, flash
from flask.ext.login import login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from models import User, Event, get_user, get_events, record_result
from simplecrypt import decrypt
from config import SECRET_KEY
import copy
import datetime as dt

with app.test_request_context('/index', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    assert request.path == '/index'
    assert request.method == 'POST'

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', user=current_user, title='Home')

@app.route('/about')
@login_required
def about():
    return render_template('about.html', title='About', user=current_user)


@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == "POST":
        name = (request.form["first-name"]+" "+request.form["last-name"])
        user = User(name)
        db.session.add(user)
        user.initialize(request.form["email"], request.form["password"])
        print "User: "+user.name+" successfully registered."
        return redirect(url_for("index"))
    return render_template('register.html', title='Register')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        user = get_user(email=request.form["email"])
        if user:
            password = request.form["password"]
            if password == decrypt(SECRET_KEY, user.password).decode('utf8'):
                remember = request.form.get("remember", "no") == "yes"
                if login_user(user, remember=remember):
                    print "Logged in."
                    return redirect(url_for("index"))
                else:
                    print "Error logging in. Please contact administrator."
            else:
                print "Incorrect password."
    return render_template('login.html', title='Sign In')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    print "Logged out."
    return redirect(url_for("login"))

@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html', title='Profile', user=current_user)

@app.route("/host", methods=["GET","POST"])
@login_required
def host():
    if request.method == "POST":
        event = request.form["event-name"]
        description = request.form["event-description"]
        datetime = get_date(request.form["datepicker"])
        event_type = request.form["event-type"]
        #print(event, description, datetime, event_type)
        e = Event(event, datetime, event_type, current_user.name, description)
        db.session.add(e)
        #db.session.commit()
        return redirect(url_for("host"))
    return render_template('host.html', title='Host Event', user=current_user, users=User.query.all())


#######################
# Helper Functions
#######################

def get_date(date):
    return dt.datetime.strptime(date, '%Y/%m/%d %H:%M')

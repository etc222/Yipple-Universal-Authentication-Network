from flask import render_template_string, request, render_template, redirect, url_for, session
from . import app
from .. import models

@app.route('/')
def home():
    return render_template("home.html")

## Get username and password from login form and call validate user from models
## returns 403 error if invalid details otherwise redirect to users page
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        outcome = models.validateUser(username, password)
        if outcome == 403:
            return "invalid login details", 403
        if outcome == 0:
            session['username'] = username
            return redirect(url_for('basic.users', account = 'me'))
        return "login request received", 400

    return render_template("login.html")

@app.route('/logout', methods=["GET"])
def logout():
    session.clear()

    return redirect(url_for("basic.home"))

## Get username and password from register form and call register user from models
## returns 400 error if invalid details otherwise redirect to login page
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        outcome = models.registerUser(username, password)
        if outcome == 0:
            return redirect(url_for('basic.login'))
        elif outcome == 400:
            return "username is taken", 400
        else:
            return "Server error", 500

    return render_template("register.html")

## Define variable account
@app.route('/users/<account>')
def users(account):
    displayAccount = session['username'] if account == 'me' else account
    return render_template("users.html", account = displayAccount)

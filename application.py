from flask import Flask, redirect, render_template, request, session, url_for
from passlib.apps import custom_app_context
from passlib.context import CryptContext
from functools import wraps
import sqlite3

conn = sqlite3.connect('cadet.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

app = Flask(__name__)

def login_required(f):
    """
    adapted from pset7 of cs50 edx course

    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "" or password == "":
            return error("please provide a username and password")
        c.execute("SELECT username FROM users WHERE username=?", (username,))
        username_exists = c.fetchone()
        if username_exists == None:
            return error("Username not found")
        c.execute("SELECT hash FROM users WHERE username=?", (username,))
        row=c.fetchone()
        verify_password=row[0]
        if not custom_app_context.verify(password,verify_password):
            return error("Username or password invalid")
        c.execute("SELECT id FROM users WHERE username=?", (username,))
        row=c.fetchone()
        get_id = row[0]
        session["user_id"] = get_id
        return redirect("/add")
    else:
        return render_template("login.html")

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method ==  "POST":
        first = request.form.get("first")
        last = request.form.get("last")
        if first == "" or last == "":
            msg = "please provide your first and last name"
            return error(msg)
        else:
            c.execute("SELECT first_name, last_name FROM cadets WHERE first_name=? AND last_name=?", (first, last))
            exists = c.fetchone()
            if exists == None:
                c.execute("INSERT INTO cadets (first_name, last_name, attendance_current_rank, attendance_total) VALUES (?, ?, 1, 1)", (first, last))
                conn.commit()
                return redirect("/add")
            else:
                msg = "this name already exists in the database"
                return error(msg)
    else:
        cadets = c.execute("SELECT * FROM cadets ORDER BY last_name DESC")
        return render_template("add.html", cadets = cadets)

def error(msg):
    return render_template("error.html", msg = msg)

@app.route("/view", methods=["GET"])
def view():
    cadets = c.execute("SELECT * FROM cadets")
    return render_template("view.html", cadets = cadets)

@app.route("/check_in/<first>,<last>")
def check_in(first, last):
    c.execute("UPDATE cadets SET attendance_current_rank = attendance_current_rank + 1, attendance_total = attendance_total + 1 WHERE first_name=? AND last_name=? and time != date('now')", (first, last))
    c.execute("UPDATE cadets SET time = date('now') WHERE first_name=? AND last_name=?", (first, last))
    conn.commit()
    return redirect("/add")

app.secret_key = "q3n$)1hsgg8@8vhwa75up9g0qdpa3f$wc1ynh$pf(aqxk^h^6s"

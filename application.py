from flask import Flask, redirect, render_template, request, session, url_for
from passlib.apps import custom_app_context
from passlib.context import CryptContext
from functools import wraps
import psycopg2
import psycopg2.extras
import os
import urllib.parse as urlparse

############
###connects to local postgresql db
############
#conn = psycopg2.connect("dbname=cadet2 user=postgres host=localhost password=postgres")
#c = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

url = urlparse.urlparse(os.environ['DATABASE_URL'])

conn = psycopg2.connect("dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
c = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

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
        c.execute("SELECT username FROM users WHERE username=%s", (username,))
        username_exists = c.fetchone()
        if username_exists == None:
            return error("Username not found")
        c.execute("SELECT hash FROM users WHERE username=%s", (username,))
        row=c.fetchone()
        verify_password=row[0]
        if not custom_app_context.verify(password,verify_password):
            return error("Username or password invalid")
        c.execute("SELECT id FROM users WHERE username=%s", (username,))
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
        first = request.form.get("first").upper()
        last = request.form.get("last").upper()
        if first == "" or last == "":
            msg = "Please provide your first and last name"
            return error(msg)
        else:
            c.execute("SELECT first_name, last_name FROM cadets WHERE first_name=%s AND last_name=%s", (first, last))
            exists = c.fetchone()
            if exists == None:
                c.execute("INSERT INTO cadets (first_name, last_name, attendance_current_rank, attendance_total) VALUES (%s, %s, 1, 1)", (first, last))
                conn.commit()
                return redirect("/add")
            else:
                msg = "This name has already been added"
                return error(msg)
    else:
        cadets = c.execute("SELECT * FROM cadets ORDER BY last_name ASC")
        row = c.fetchall()
        return render_template("add.html", cadets = row)


@app.route("/edit", methods = ["GET", "POST"])
@login_required
def edit():
    if request.method == "POST":
        return error("wow you got here by post somehow")
    else:
        cadets = c.execute("SELECT * FROM cadets ORDER BY last_name ASC")
        row = c.fetchall()
        return render_template("edit.html", cadets = row)



@app.route("/view", methods=["GET"])
def view():
    cadets = c.execute("SELECT * FROM cadets ORDER BY last_name ASC")
    row=c.fetchall()
    return render_template("view.html", cadets = row)



@app.route("/check_in/<first>,<last>")
def check_in(first, last):
    c.execute("UPDATE cadets SET attendance_current_rank = attendance_current_rank + 1, attendance_total = attendance_total + 1 WHERE first_name=%s AND last_name=%s AND time != date('now')", (first, last))
    c.execute("UPDATE cadets SET time = date('now') WHERE first_name=%s AND last_name=%s", (first, last))
    conn.commit()
    confirm = first.capitalize() + " " + last.capitalize() + " checked in"
    cadets = c.execute("SELECT * FROM cadets ORDER BY last_name ASC")
    row=c.fetchall()
    return render_template("add.html", confirm = confirm, cadets = row)



@app.route("/adjust_rank/<first>,<last>", methods=["GET", "POST"])
@login_required
def adjust_rank(first, last):
    if request.method == "POST":
        first_from_form=request.form.get("first")
        last_from_form=request.form.get("last")
        set_belt=request.form.get("belt")
        set_stripes=int(request.form.get("stripes"))
        c.execute("SELECT attendance_current_rank FROM cadets WHERE first_name=%s AND last_name=%s", (first_from_form, last_from_form))
        row=c.fetchone()
        saved_progress = row[0]
        if saved_progress < 100:
            saved_progress = saved_progress % 25
        else: 
            saved_progress = 0
        set_stripes=set_stripes * 25 + saved_progress
        c.execute("UPDATE cadets SET rank=%s, attendance_current_rank=%s WHERE first_name=%s AND last_name=%s", (set_belt, set_stripes, first_from_form, last_from_form))
        conn.commit()
        return redirect("/edit")
    else:
        c.execute("SELECT rank FROM cadets WHERE first_name=%s AND last_name=%s", (first, last))
        row=c.fetchone()
        belt=row[0]
        c.execute("SELECT attendance_current_rank FROM cadets WHERE first_name=%s AND last_name=%s", (first, last))
        row=c.fetchone()
        stripes=(row[0]-(row[0]%25))/25
        if stripes > 4:
            stripes=4
        return render_template("adjust_rank.html", first=first, last=last, belt=belt, stripes=stripes)



@app.route("/delete/<first>,<last>", methods=["GET", "POST"])
@login_required
def delete(first,last):
    if request.method == "POST":
        first_from_form=request.form.get("first")
        last_from_form=request.form.get("last")
        c.execute("DELETE FROM cadets WHERE first_name = %s AND last_name = %s", (first_from_form, last_from_form))
        conn.commit()
        return redirect("/edit")
    else:
        return render_template("delete.html", first=first, last=last)



def error(msg):
    return render_template("error.html", msg = msg)



app.secret_key = "q3n$)1hsgg8@8vhwa75up9g0qdpa3f$wc1ynh$pf(aqxk^h^6s"

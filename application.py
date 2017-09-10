from flask import Flask, redirect, render_template, request, session, url_for
import sqlite3
conn = sqlite3.connect('cadet.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method ==  "POST":
        first = request.form.get("first")
        last = request.form.get("last")
        if first == "" or last == "":
            msg = "please provide your first and last name"
            return error(msg)
        else:
            lookup = c.execute("SELECT first_name, last_name FROM cadets WHERE first_name=? AND last_name=?", (first, last))
            exists = c.fetchone()
            if exists is None:
                c.execute("INSERT INTO cadets (first_name, last_name, attendance_current_rank, attendance_total) VALUES (?, ?, 1, 1)", (first, last))
                conn.commit()
                return redirect("/add")
            else:
                msg = "this name already exists in the database"
                return error(msg)
    else:
        cadets = c.execute("SELECT * FROM cadets")
        return render_template("add.html", cadets = cadets)

def error(msg):
    return render_template("error.html", msg = msg)


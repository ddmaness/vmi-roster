from flask import Flask, redirect, render_template, request, session, url_for
import sqlite3
conn = sqlite3.connect('cadet.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method ==  "POST":
        first = request.form.get("first")
        last = request.form.get("last")
        c.execute("INSERT INTO cadets (first_name, last_name, attendance_current_rank, attendance_total) VALUES (?, ?, 1, 1)", (first, last))
        conn.commit()
        return redirect("/")
    else:
        cadets = c.execute("SELECT * FROM cadets")
        return render_template("index.html", cadets = cadets)
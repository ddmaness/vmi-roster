from flask import Flask, redirect, render_template, request, session, url_for
import sqlite3
conn = sqlite3.connect('cadet.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

app = Flask(__name__)

@app.route("/")
def index():
    cadets = c.execute("SELECT * FROM cadets")
    return render_template("index.html", cadets = cadets)
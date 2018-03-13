import os
from flask import Flask, redirect, render_template, request
from flask_socketio import SocketIO, emit

import Channel
import Flacker



app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        #get username and password from login form
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        repassword = request.form.get("repassword")   
        return render_template("login.html") 

@app.route("/chat", methods=["GET", "POST"])
def chat():

    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        return render_template("login.html")
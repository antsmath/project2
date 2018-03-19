import os
from flask import Flask, redirect, render_template, request, url_for, session
from flask_session import Session
from flask_socketio import SocketIO, emit

from Channel import Channel
from Flacker import Flacker

#create flackers and channels
flackers = {}
channels = set([Channel('Main', 100)])

#config
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
socketio = SocketIO(app)

# Configure session to use filesystem
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if session.get('user_name') is not None:
        return redirect(url_for('chat'))

    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        #get username and password from login/registration form
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        new_flacker = Flacker(user_name, password)

        #check login
        if repassword is None:
            if user_name in flackers and new_flacker == flackers[user_name]:
                session['user_name'] = user_name
                return redirect(url_for('chat'))

            else:
                return render_template('login_error.html', message='Username Password combination was not valid.')

        #check registration if passwords match
        elif not password == repassword:
            return render_template('login_error.html', message='Password did not match Re-typed password.')

        #check if flacker already exist
        elif user_name in flackers:
            return render_template('login_error.html', message='That username is already used.')

        else:
            flackers[user_name] = new_flacker
            session['user_name'] = user_name
            return redirect(url_for('chat', channel='Main'))


@app.route('/chat', methods=['GET', 'POST'])
def chat_no_room():
    return redirect(url_for('chat', channel='Main'))


@app.route('/chat/<string:channel>', methods=['GET', 'POST'])
def chat(channel):

    #check if user_name is logged in
    if session.get('user_name') is None:
        return redirect(url_for('index'))

    else:
        user_name = session.get('user_name')
        if request.method == 'GET':
            return render_template('chat.html', channels=channels, user_name=user_name, channel=channel)

        if request.method == 'POST':
            return render_template('chat.html', channels=channels,  user_name=user_name, channel=channel)

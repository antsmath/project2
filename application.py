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
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    # remove current flacker if one is available
    session.clear()

    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        #get username and password from login/registration form
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        last_channel = request.form.get('last_channel')
        new_flacker = Flacker(user_name, password)

        #check login
        if repassword is None:
            if user_name in flackers and new_flacker == flackers[user_name]:
                session['user_name'] = user_name
                return redirect(url_for('chat', channel=last_channel))

            else:
                return render_template('login_error.html', message='Username Password combination was not valid.')

        #check registration if passwords match
        elif not password == repassword:
            return render_template('login_error.html', message='Password did not match Re-typed password.')

        #check if flacker already exist
        elif user_name in flackers:
            return render_template('login_error.html', message=f'The username, {user_name}, is already used.')

        else:
            flackers[user_name] = new_flacker
            session['user_name'] = user_name
            return redirect(url_for('chat', channel='Main'))


@app.route('/chat')
def chat_no_channel():
    return redirect(url_for('index'))


@app.route('/chat/<string:channel>', methods=['GET', 'POST'])
def chat(channel):

    #check if flacker is logged in
    if session.get('user_name') is None:
        return redirect(url_for('index'))

    else:
        user_name = session.get('user_name')
        if request.method == 'GET':
            return render_template('chat.html', channels=channels, user_name=user_name, channel=channel)

        elif request.method == 'POST':
            return render_template('chat.html', channels=channels,  user_name=user_name, channel=channel)

@app.route('/chat/new_channel', methods=['GET', 'POST'])
def new_channel():

    #check if flacker is logged in
    if session.get('user_name') is None:
        return redirect(url_for('index'))

    else:
        if request.method == 'GET':
            return render_template('new_channel.html')

        elif request.method == 'POST':
            channel_name = request.form.get('channel_name')
            new_channel = Channel(channel_name, 100)
             
            if channel_name is None:
                return render_template('new_channel_error.html', message='Channel Name field required')

            elif new_channel in channels:
                return render_template('new_channel_error.html', message=f'Channel Name, {channel_name}, already exist.')

            else:
                channels.add(new_channel)
                return redirect(url_for('chat', channel=channel_name))

# #Enter a channel
# @socketio.on('enter channel')
# def enter_channel(sid, data):
#     socketio.enter_room(sid, data['room'])

# #Leave a channel
# @socketio.on('leave channel')
# def leave_channel(sid, data):
#     socketio.leave_room(sid, data['room'])

# #Send a message to a channel
# @socketio.on('submit message')
# def post_messsage(sid, damessageta, channel):
#     socketio.emit('post message', message, room=channel)

#Send a message to a channel
@socketio.on('submit message')
def post_messsage(data):
    message = data['message']
    print(message)
    emit('post message', {'message': message}, broadcast=True)
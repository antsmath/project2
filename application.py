import os
from flask import Flask, redirect, render_template, request, url_for, session
from flask_session import Session
from flask_socketio import SocketIO, emit, join_room, leave_room

from Channel import Channel
from Flacker import Flacker

#create flackers and channels
flackers = {}
channels = set([Channel('Main', 100)])
flackers_in_channels = []

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

#Enter a channel
@socketio.on('enter channel')
def enter_channel(data):
    user_name = data['user_name']
    channel = data['channel']
    join_room(channel)

    #check if flacker is already in channel (such as a different tab)
    if not {user_name, channel} in flackers_in_channels:
        emit('post join', {
            'message': f'{user_name} has joined {channel}!'}, room=channel, broadcast=True)

    #add flacker to channel
    flackers_in_channels.append({user_name, channel})

#Leave a channel
@socketio.on('leave channel')
def leave_channel(data):
    user_name = data['user_name']
    channel = data['channel']
    leave_room(channel)
    print({user_name, channel} in flackers_in_channels)

    #Remove flacker from first instance in channel
    try:
        flackers_in_channels.remove({user_name, channel})
    except:
        print(f'{user_name} was not found in {channel}.')
    print({user_name, channel} in flackers_in_channels)

    #Check if user is still in channel from another area (such as a different tab)
    if not {user_name, channel} in flackers_in_channels:
        emit('post leave', {
             'message': f'{user_name} has left {channel}.'}, room=channel, broadcast=True)

#Send a message to a channel
@socketio.on('submit message')
def post_messsage(data):
    message = data['message']
    channel = data['channel']
    emit('post message', {'message': message}, room=channel, broadcast=True)

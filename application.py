import os
import json
from flask import Flask, redirect, render_template, request, url_for, session
from flask_session import Session
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime
from time import strftime


from Channel import Channel
from Flacker import Flacker

#create flackers and channels
flackers = {}
channels = [Channel('Main', 100)]
flackers_in_channels = []

#config
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
socketio = SocketIO(app)

# Configure session to use filesystem
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
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
    return redirect(url_for('login'))


@app.route('/chat/<string:channel>')
def chat(channel):

    temp_channel = Channel(channel, 0)
    #check if flacker is logged in
    # if session.get('user_name') is None:
    #     return redirect(url_for('login'))

    #check if channel exist
    if temp_channel not in channels:
        return redirect(url_for('chat', channel='Main'))

    else:
        user_name = session.get('user_name')
        ind = channels.index(temp_channel)
        return render_template('chat.html', channel_messages=channels[ind].messages, user_name=user_name, channel=channel)


@app.route('/chat/new_channel', methods=['GET', 'POST'])
def new_channel():

    #check if flacker is logged in
    if session.get('user_name') is None:
        return redirect(url_for('login'))

    else:
        if request.method == 'GET':
            return render_template('new_channel.html')

        #create channel
        elif request.method == 'POST':
            channel_name = request.form.get('channel_name')
            new_channel = Channel(channel_name, 100)

            #validate form is filled
            if channel_name is None:
                return render_template('new_channel_error.html', message='Channel Name field required')

            #validate channel_name has valid characters
            elif not channel_name.isalnum():
                return render_template('new_channel_error.html', message=f'Channel Name, {channel_name}, contained invalid characters.')

            #check if channel already exist
            elif new_channel in channels:
                return render_template('new_channel_error.html', message=f'Channel Name, {channel_name}, already exist.')

            #create channel and load channel
            else:
                channels.append(new_channel)
                return redirect(url_for('chat', channel=channel_name))


@socketio.on('enter channel')
#Enter a channel
def enter_channel(data):
    user_name = data['user_name']
    channel = data['channel']
    timestamp = datetime.now().strftime('%x %X')
    message = f'{user_name} has joined {channel}!'

    join_room(channel)

    #check if flacker is already in channel (such as a different tab)
    if {user_name, channel} not in flackers_in_channels:
        temp_channel = Channel(channel, 0)
        try:
            ind = channels.index(temp_channel)
            emit('post join', {'user_name': user_name, 'message': message,
                               'timestamp': timestamp}, room=channel, broadcast=True)
            channels[ind].add_message(user_name, message, timestamp)
        except:
            print(f'Channel {channel} not found, unable to add user.')

    #add flacker to channel
    flackers_in_channels.append({user_name, channel})


@socketio.on('leave channel')
#Leave a channel
def leave_channel(data):
    user_name = data['user_name']
    channel = data['channel']
    timestamp = datetime.now().strftime('%x %X')
    leave_room(channel)
    message = f'{user_name} has left {channel}.'

    #Remove flacker from first instance in channel
    try:
        flackers_in_channels.remove({user_name, channel})
    except:
        print(f'{user_name} was not found in {channel}.')

    #Check if user is still in channel from another area (such as a different tab)
    if {user_name, channel} not in flackers_in_channels:
        temp_channel = Channel(channel, 0)
        try:
            ind = channels.index(temp_channel)
            emit('post leave', {'user_name': user_name, 'message': message,
                                'timestamp': timestamp}, room=channel, broadcast=True)
            channels[ind].add_message(user_name, message, timestamp)
        except:
            print(f'Channel {channel} not found, unable to remove user.')


@socketio.on('submit message')
#Send a message to a channel
def post_messsage(data):
    user_name = data['user_name']
    message = data['message']
    timestamp = datetime.now().strftime('%x %X')
    channel = data['channel']
    temp_channel = Channel(channel, 0)
    try:
        ind = channels.index(temp_channel)
        emit('post message', {'user_name': user_name, 'message': message,
                              'timestamp': timestamp}, room=channel, broadcast=True)
        channels[ind].add_message(user_name, message, timestamp)
    except:
        print(f'Channel {channel} not found, unable to post message.')


@app.route('/get_channels/<string:channel>')
#Return list of channels
def get_channels(channel):
        return render_template('channel_list.html', channels=channels, channel=channel)

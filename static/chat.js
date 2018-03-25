const current_script = document.currentScript;

document.addEventListener('DOMContentLoaded', () => {
    // Store user_name and last_channel accessed
    const data_user_name = current_script.getAttribute('data-user-name');
    const data_channel = current_script.getAttribute('data-channel')
    localStorage.setItem('user_name', data_user_name);
    localStorage.setItem('last_channel', data_channel);

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // Join channel
    socket.emit('enter channel', { 'user_name': data_user_name, 'channel': data_channel });

    // When connected, configure buttons
    socket.on('connect', () => {
        // Submit message in chat box
        document.getElementById('submit').onclick = (event) => {
            const message = document.getElementById('text').value;
            if (message.length > 0) {
                socket.emit('submit message', { 'user_name': data_user_name, 'message': message, 'channel': data_channel });
                // Clear field
                document.getElementById('text').value = ''
                event.preventDefault();
            };
        }
    });

    // Add message to channel for other users when user submits message
    socket.on('post message', data => {
        const li = document.createElement('li');
        li.innerHTML = `${data.message}`;
        document.getElementById('messages').append(li);
    });

    // Add message to channel when user joins
    socket.on('post join', data => {
        const li = document.createElement('li');
        li.innerHTML = `${data.message}`;
        document.getElementById('messages').append(li);
    });

    // Add message to channel when user leaves page
    socket.on('post leave', data => {
        const li = document.createElement('li');
        li.innerHTML = `${data.message}`;
        document.getElementById('messages').append(li);
    });

    // Exit channel when leaving page
    window.addEventListener("beforeunload", () => {
        socket.emit('leave channel', { 'user_name': data_user_name, 'channel': data_channel });
    });

});
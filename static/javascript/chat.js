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

    // // Add message to channel for other users when user submits message
    // socket.on('post message', data => {
    //     const li = document.createElement('li');
    //     li.innerHTML = `${data.message}`;
    //     document.getElementById('messages').append(li);
    // });

    // Add message to channel for other users when user submits message
    socket.on('post message', data => {
        const card = document.createElement('div');
        card.classList.add('card');
        card.classList.add('text');
        card.classList.add('center');
        card.classList.add('rounded');
        card.innerHTML = `${data.message}`;
        document.getElementById('messages').append(card);
    });

    // Add message when user presses enter on text box
    document.getElementById('text').addEventListener("keyup", (event) => {
        event.preventDefault();
        if (event.keyCode === 13) {
            document.getElementById("submit").click();
        }
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

    // Start scrollbar at last message
    window.onload = () => {
        document.getElementById('main').scrollTop = document.getElementById('main').scrollHeight;
    };

    // Exit channel when leaving page
    window.addEventListener('beforeunload', () => {
        socket.emit('leave channel', { 'user_name': data_user_name, 'channel': data_channel });
    });

    // Operate Navbar
    let is_nav_open = false;
    document.getElementById('other_channel_nav').onclick = () => {
        // Close Navbar
        if (is_nav_open) {
            document.getElementById('Side_Nav').style.width = '0';
            document.getElementById('header').style.marginLeft = '0';
            document.getElementById('main').style.marginLeft = '0';
            document.getElementById('chat-text').style.marginLeft = '0';
            is_nav_open = false;
        }
        // Open Navbar
        else {
            document.getElementById('Side_Nav').style.width = '250px';
            document.getElementById('header').style.marginLeft = '250px';
            document.getElementById('main').style.marginLeft = '250px';
            document.getElementById('chat-text').style.marginLeft = '250px';
            is_nav_open = true;
        }

    };

    // Close Navbar
    document.getElementById('close_nav').onclick = () => {
        document.getElementById('Side_Nav').style.width = '0';
        document.getElementById('header').style.marginLeft = '0';
        document.getElementById('main').style.marginLeft = '0';
        document.getElementById('chat-text').style.marginLeft = '0';
        is_nav_open = false;
    }

});
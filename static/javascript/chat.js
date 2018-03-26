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
        card = create_card(`${data.user_name}`, `${data.message}`, `${data.timestamp}`);
        document.getElementById('messages').append(card);
        document.getElementById('main').scrollTop = document.getElementById('main').scrollHeight;
    });

    // Add message when user presses enter on text box
    document.getElementById('text').addEventListener("keydown", (event) => {
        if (event.keyCode === 13 && !event.shiftKey) {
            event.preventDefault();
            document.getElementById("submit").click();
        }
    });

    // Add message to channel when user joins
    socket.on('post join', data => {
        card = create_card(`${data.user_name}`, `${data.message}`, `${data.timestamp}`);
        document.getElementById('messages').append(card);
        document.getElementById('main').scrollTop = document.getElementById('main').scrollHeight;
    });

    // Add message to channel when user leaves page
    socket.on('post leave', data => {
        card = create_card(`${data.user_name}`, `${data.message}`, `${data.timestamp}`);
        document.getElementById('messages').append(card);
        document.getElementById('main').scrollTop = document.getElementById('main').scrollHeight;
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
            load_channels();
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

    // Load channels for navbar.
    function load_channels() {
        const request = new XMLHttpRequest();
        request.open('GET', `/get_channels` + '/' + data_channel);
        request.onload = () => {
            // const response = request.responseText;
            const response = request.responseText;
            document.getElementById('channel_list').innerHTML = response;
        };
        request.send();
    }

    // Logout removes last channel
    document.getElementById('logout').addEventListener('click', () => {
         localStorage.removeItem('last_channel'); 
    });

});

function create_card(user_name, message, timestamp) {
    //create head of card
    const card_title = document.createElement('h5');
    card_title.classList.add('card-title');
    card_title.textContent = user_name;

    //create body of card
    const card_text = document.createElement('p');
    card_text.classList.add('card-text');
    //save formatting of return characters
    var paragraphs = message.split('\n');
    for (var i = 0, l = paragraphs.length; i < l; i++) {
        card_text.textContent += paragraphs[i] + '\r\n';
    }

    //create timestamp of card
    const card_footer = document.createElement('p');
    card_footer.classList.add('card-timestamp');
    card_footer.textContent = timestamp;

    //create card
    const card = document.createElement('div');
    card.classList.add('card');
    card.classList.add('text');
    card.classList.add('center');
    card.classList.add('rounded');
    card.append(card_title);
    card.append(card_text);
    card.append(card_footer);

    return card;
}


document.addEventListener('DOMContentLoaded', () => {
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {

        // Get message in chat box
        document.getElementById('submit').onclick = () => {
            const message = document.getElementById('text').value;
            event.preventDefault();
            socket.emit('submit message', { 'message': message});
        };
    });

    // When a new vote is announced, add to the unordered list
    socket.on('post message', data => {
        const li = document.createElement('li');
        console.log(`test`)
        console.log(`Vote recorded: ${data.message}`)
        li.innerHTML = `Vote recorded: ${data.message}`;
        document.getElementById('votes').append(li);
    });
});
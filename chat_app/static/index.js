const socket = io('http://' + document.domain + ':' + location.port);
socket.on('connect', async () => {
    const current_user = await get_current_user();
    if (current_user) {
        socket.emit('event', {
            message: `${current_user.nickname} connected to server!`,
            connect: true,
        });
    }

    const sendButton = document.getElementById('send_btn');
    sendButton.addEventListener('click', async (event) => {
        event.preventDefault();
        const messageInput = document.getElementById("message_text");
        const message = messageInput.value;

        if (message) {
            socket.emit('event', {
                message,
                current_user,
            })
            messageInput.value = '';
        }
    });
});

socket.on('message response', (data) => {
    add_message(data)
})

add_message = async (data) => {
    const current_user = await get_current_user();
    const messages = document.getElementById('messages');
    const card = document.createElement('div');
    card.className = `card text-white ${data.current_user.id === current_user.id ? 'bg-secondary' : 'bg-info'} mb-3`;
    messages.appendChild(card);
    const card_body = document.createElement('div');
    card_body.className='card-body'
    card.appendChild(card_body);
    const card_title = document.createElement('h5');
    card_title.className='card-subtitle'
    card_title.innerText = data.current_user.nickname;
    card_body.appendChild(card_title);
    const card_text = document.createElement('p');
    card_text.className = 'card-text';
    card_text.innerText = data.message;
    card_body.appendChild(card_text);
}

get_current_user = async () => {
    return await fetch('/get_current_user')
        .then(async (response) => {
            return await response.json();
        }).then((data) => {
            return data;
        });
}
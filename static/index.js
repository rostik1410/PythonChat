const socket = io('http://' + document.domain + ':' + location.port);
socket.on('connect', async () => {
    const nickname = await get_nickname();
    if (nickname) {
        socket.emit('event', {
            message: `${nickname} connected to server!`,
            nickname,
            connect: true,
        });
    }

    const sendButton = document.getElementById('send_btn');
    sendButton.addEventListener('click', async (event) => {
        console.log('check')
        event.preventDefault();
        const messageInput = document.getElementById("message_text");
        const message = messageInput.value;
        socket.emit('event', {
            message,
            nickname,
        })
        messageInput.value = '';
    });
});

socket.on('message response', (data) => {
    add_message(data)
})

window.onload = async () => {
    get_messages();
}

add_message = (data) => {
    console.log('data', data)
    const curr_message = document.createElement('li');
    curr_message.innerText = `${data.nickname} - ${data.message}`;
    const messages = document.getElementById('messages');
    messages.appendChild(curr_message);
}

async function get_nickname () {
    return await fetch('/get_nickname')
        .then( async (response) => {
            return await response.json();
        }).then((data) => {
            return data.nickname;
        });
}

get_messages = () => {
    console.log('get_messages');
}
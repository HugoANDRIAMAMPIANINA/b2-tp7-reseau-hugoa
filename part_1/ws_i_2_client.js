const websocket = new WebSocket('ws://localhost:8765');

websocket.onmessage = (event) => {
    messageReceived = event.data + "\n";
    const history = document.getElementById('history');
    const message = document.createElement('p');
    const text = document.createTextNode(messageReceived)
    message.appendChild(text);
    history.appendChild(message);
}

document.getElementById("inputForm").addEventListener('submit', async (event) => {
    event.preventDefault();
    const message = document.getElementById('userMessage');
    await websocket.send(message.value);
    message.value = '';
});

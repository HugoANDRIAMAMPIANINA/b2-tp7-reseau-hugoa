const websocket = new WebSocket('ws://localhost:8765');

websocket.onmessage = (event) => {
    data = JSON.parse(event.data)
    clientUsername = data.username
    clientMessage = data.message;
    const history = document.getElementById('history');
    const label = document.createElement('label');
    const message = document.createElement('p');
    const text = document.createTextNode(" : " + clientMessage)
    label.appendChild(document.createTextNode(clientUsername))
    label.style.color = "#" + data.color
    message.appendChild(label)
    message.appendChild(text);
    history.appendChild(message);
}

document.getElementById("inputForm").addEventListener('submit', async (event) => {
    event.preventDefault();
    const username = document.getElementById('username');
    const message = document.getElementById('userMessage');
    const data = { username: username.value, message: message.value }
    await websocket.send(JSON.stringify(data));
    userMessage.value = '';
});

websocket.onclose = function() {
    console.log('WebSocket client disconnected');
    
};
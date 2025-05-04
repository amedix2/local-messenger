document.addEventListener('DOMContentLoaded', function() {
    let username = sessionStorage.getItem('username');
    if (!username) {
        username = prompt('Please enter your username:');
        if (username) {
            sessionStorage.setItem('username', username);
        } else {
            alert('Username is required.');
            return;
        }
    }
    document.getElementById('username').textContent = username;

    function fetchMessages() {
        fetch('/get_messages')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    renderMessages(data.status);
                } else {
                    console.error('Failed to fetch messages:', data.error);
                }
            })
            .catch(error => console.error('Error fetching messages:', error));
    }

    function renderMessages(messages) {
        const messagesDiv = document.getElementById('messages');
        messagesDiv.innerHTML = '';
        messages.forEach(message => {
            const [text, username, time] = message;
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message');
            if (username === sessionStorage.getItem('username')) {
                messageDiv.classList.add('own-message');
            }
            messageDiv.innerHTML = `
                <div class="message-header">
                    <span class="username">${username}</span>
                    <span class="time">${new Date(time).toLocaleTimeString()}</span>
                </div>
                <div class="message-text">${text}</div>
            `;
            messagesDiv.appendChild(messageDiv);
        });
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    fetchMessages();
    setInterval(fetchMessages, 1000);

    document.getElementById('message-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const messageInput = document.getElementById('message-input');
        const text = messageInput.value.trim();
        if (text) {
            fetch('/add_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({text: text, username: username})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    messageInput.value = '';
                    fetchMessages();
                } else {
                    console.error('Failed to add message:', data.error);
                }
            })
            .catch(error => console.error('Error adding message:', error));
        }
    });
});
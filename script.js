const chatContainer = document.getElementById('chatContainer');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');

// Add event listener for Enter key
userInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

async function sendMessage() {
    const message = userInput.value.trim();
    
    if (!message) return;
    
    // Disable input while processing
    userInput.disabled = true;
    sendButton.disabled = true;
    
    // Add user message
    addMessage(message, 'user');
    userInput.value = '';
    
    // Add loading message
    const loadingId = addLoadingMessage();
    
    try {
        const response = await fetch('http://localhost:8080/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: message })
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        
        // Remove loading message
        removeLoadingMessage(loadingId);
        
        // Add bot response
        addMessage(data.answer, 'bot');
        
    } catch (error) {
        console.error('Error:', error);
        removeLoadingMessage(loadingId);
        addMessage('Sorry, I encountered an error connecting to the server. Please make sure the backend is running on port 8080.', 'bot');
    }
    
    // Re-enable input
    userInput.disabled = false;
    sendButton.disabled = false;
    userInput.focus();
}

function addMessage(content, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    if (sender === 'user') {
        messageContent.innerHTML = `<strong>You:</strong> ${escapeHtml(content)}`;
    } else {
        messageContent.innerHTML = `<strong>Assistant:</strong> ${formatBotMessage(content)}`;
    }
    
    messageDiv.appendChild(messageContent);
    chatContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function addLoadingMessage() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.id = 'loading-message';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content loading';
    messageContent.innerHTML = '<strong>Assistant:</strong> Thinking';
    
    messageDiv.appendChild(messageContent);
    chatContainer.appendChild(messageDiv);
    
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    return 'loading-message';
}

function removeLoadingMessage(loadingId) {
    const loadingMessage = document.getElementById(loadingId);
    if (loadingMessage) {
        loadingMessage.remove();
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatBotMessage(content) {
    // Convert newlines to <br> tags
    return escapeHtml(content).replace(/\n/g, '<br>');
}

// Focus on input when page loads
window.addEventListener('load', function() {
    userInput.focus();
});
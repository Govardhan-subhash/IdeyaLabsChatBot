document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const themeToggle = document.getElementById('theme-toggle');
    
    // Theme Toggling
    themeToggle.addEventListener('click', () => {
        const body = document.body;
        if (body.getAttribute('data-theme') === 'dark') {
            body.removeAttribute('data-theme');
            themeToggle.textContent = '🌙';
        } else {
            body.setAttribute('data-theme', 'dark');
            themeToggle.textContent = '☀️';
        }
    });

    // Auto-resize input (optional enhancement)
    
    // Send Message Function
    window.sendMessage = async () => {
        const query = userInput.value.trim();
        if (!query) return;

        // Disable input
        userInput.value = '';
        userInput.disabled = true;
        sendBtn.disabled = true;

        // Add User Message
        addMessage(query, 'user');

        // Add Typing Indicator
        const typingId = addTypingIndicator();
        scrollToBottom();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: query })
            });

            const data = await response.json();
            
            // Remove Typing Indicator
            removeTypingIndicator(typingId);

            if (data.result) {
                addMessage(data.result, 'bot');
            } else if (data.error) {
                addMessage("Sorry, I encountered an error: " + data.error, 'bot');
            }
        } catch (error) {
            removeTypingIndicator(typingId);
            addMessage("Network error. Please try again later.", 'bot');
            console.error('Error:', error);
        } finally {
            userInput.disabled = false;
            sendBtn.disabled = false;
            userInput.focus();
            scrollToBottom();
        }
    };

    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        contentDiv.textContent = text; // Safe text insertion
        
        const timestampDiv = document.createElement('div');
        timestampDiv.classList.add('message-timestamp');
        const now = new Date();
        timestampDiv.textContent = now.getHours() + ':' + String(now.getMinutes()).padStart(2, '0');

        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timestampDiv);
        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }

    function addTypingIndicator() {
        const id = 'typing-' + Date.now();
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('typing-indicator');
        typingDiv.id = id;
        typingDiv.style.display = 'block';
        
        typingDiv.innerHTML = `
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
        `;
        
        chatMessages.appendChild(typingDiv);
        return id;
    }

    function removeTypingIndicator(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});

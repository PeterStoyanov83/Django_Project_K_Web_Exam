document.addEventListener('DOMContentLoaded', function () {
    const chatbot = document.getElementById('chatbot');
    const chatBubble = document.querySelector('.chatbot-bubble');
    const openChatBtn = document.getElementById('open-chat');
    const closeChatBtn = document.getElementById('close-chat');
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    let currentThreadId = null;

    function addMessage(content, type = 'bot') {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');

        switch (type) {
            case 'user':
                messageDiv.classList.add('user-message');
                break;
            case 'error':
                messageDiv.classList.add('error-message');
                break;
            default:
                messageDiv.classList.add('bot-message');
        }

        messageDiv.textContent = content;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function handleError(error, errorType) {
        let errorMessage;
        switch (errorType) {
            case 'configuration_error':
                errorMessage = "Sorry, the chat service is not properly configured. Please try again later.";
                break;
            case 'validation_error':
                errorMessage = "Please enter a valid message.";
                break;
            case 'api_error':
                errorMessage = "Sorry, I'm having trouble connecting right now. Please try again later.";
                break;
            default:
                errorMessage = "An unexpected error occurred. Please try again later.";
        }
        addMessage(errorMessage, 'error');
    }

    openChatBtn.addEventListener('click', () => {
        chatBubble.classList.add('active');
        openChatBtn.style.display = 'none';
        if (chatMessages.children.length === 0) {
            addMessage("Hi! I'm Daisy, your Project K assistant. How can I help you today?");
        }
    });

    closeChatBtn.addEventListener('click', () => {
        chatBubble.classList.remove('active');
        openChatBtn.style.display = 'block';
    });

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const userMessage = userInput.value.trim();
        if (userMessage) {
            addMessage(userMessage, 'user');
            userInput.value = '';
            userInput.disabled = true;

            try {
                const response = await fetch('/api/chat/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        message: userMessage,
                        thread_id: currentThreadId
                    }),
                });

                const data = await response.json();

                if (!response.ok) {
                    throw {message: data.error, type: data.type};
                }

                currentThreadId = data.thread_id;
                addMessage(data.message);
            } catch (error) {
                console.error('Error:', error);
                handleError(error.message, error.type);
            } finally {
                userInput.disabled = false;
                userInput.focus();
            }
        }
    });

    // Function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});


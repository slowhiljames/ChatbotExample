// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeChat();
    setupEventListeners();
    loadInitialSuggestions();
});

// Global state
let isWaitingForResponse = false;

// Initialize chat
function initializeChat() {
    const welcomeTime = document.getElementById('welcomeTime');
    welcomeTime.textContent = getCurrentTime();
    autoResizeTextarea();
}

// Setup event listeners
function setupEventListeners() {
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');

    // Send button click
    sendButton.addEventListener('click', sendMessage);

    // Enter key to send (Shift+Enter for new line)
    userInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Auto-resize textarea
    userInput.addEventListener('input', autoResizeTextarea);
}

// Auto-resize textarea based on content
function autoResizeTextarea() {
    const textarea = document.getElementById('userInput');
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
}

// Load initial suggestions
async function loadInitialSuggestions() {
    try {
        const response = await fetch('/initial-suggestions');
        const data = await response.json();
        displaySuggestions(data.suggestions, 'initialSuggestions');
    } catch (error) {
        console.error('Error loading suggestions:', error);
    }
}

// Send message
async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();

    if (!message || isWaitingForResponse) return;

    // Clear input and reset height
    userInput.value = '';
    autoResizeTextarea();

    // Display user message
    displayUserMessage(message);

    // Remove initial suggestions if present
    const initialSuggestions = document.getElementById('initialSuggestions');
    if (initialSuggestions) {
        initialSuggestions.remove();
    }

    // Show typing indicator
    showTypingIndicator();
    isWaitingForResponse = true;

    try {
        // Send to backend
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        // Hide typing indicator
        hideTypingIndicator();
        isWaitingForResponse = false;

        // Display bot response
        displayBotMessage(data.response, data.suggestions || []);

    } catch (error) {
        hideTypingIndicator();
        isWaitingForResponse = false;
        displayBotMessage('Sorry, I encountered an error. Please try again.', []);
        console.error('Error:', error);
    }
}

// Display user message
function displayUserMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-text">
                <p>${escapeHtml(message)}</p>
            </div>
            <div class="message-time">${getCurrentTime()}</div>
        </div>
        <div class="message-avatar"></div>
    `;

    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Display bot message
function displayBotMessage(message, suggestions = []) {
    const chatMessages = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.innerHTML = `
        <div class="message-avatar">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/>
            </svg>
        </div>
        <div class="message-content">
            <div class="message-text">
                <p>${escapeHtml(message)}</p>
            </div>
            <div class="message-time">${getCurrentTime()}</div>
        </div>
    `;

    chatMessages.appendChild(messageDiv);

    // Add suggestions if any
    if (suggestions && suggestions.length > 0) {
        const suggestionsDiv = document.createElement('div');
        suggestionsDiv.className = 'suggestions-container';
        suggestionsDiv.innerHTML = `
            <p class="suggestions-label">💡 You might also ask:</p>
            <div class="suggestions" id="suggestions-${Date.now()}"></div>
        `;
        chatMessages.appendChild(suggestionsDiv);
        
        const suggestionsContainer = suggestionsDiv.querySelector('.suggestions');
        displaySuggestions(suggestions, suggestionsContainer);
    }

    scrollToBottom();
}

// Display suggestion chips
function displaySuggestions(suggestions, container) {
    const suggestionsContainer = typeof container === 'string' 
        ? document.getElementById(container).querySelector('.suggestions')
        : container;

    if (!suggestionsContainer) return;

    suggestionsContainer.innerHTML = '';
    suggestions.forEach(suggestion => {
        const chip = document.createElement('button');
        chip.className = 'suggestion-chip';
        chip.textContent = suggestion;
        chip.addEventListener('click', () => {
            document.getElementById('userInput').value = suggestion;
            sendMessage();
        });
        suggestionsContainer.appendChild(chip);
    });
}

// Show typing indicator
function showTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    const chatMessages = document.getElementById('chatMessages');
    
    typingIndicator.style.display = 'flex';
    chatMessages.appendChild(typingIndicator);
    scrollToBottom();
}

// Hide typing indicator
function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    typingIndicator.style.display = 'none';
}

// Scroll to bottom
function scrollToBottom() {
    const chatMessages = document.getElementById('chatMessages');
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 100);
}

// Get current time
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    });
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Focus input on load
window.addEventListener('load', () => {
    document.getElementById('userInput').focus();
});

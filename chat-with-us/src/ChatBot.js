import { useEffect, useRef, useState } from 'react';
import './ChatBot.css';

const ChatBot = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState('checking');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Check server health on mount
  useEffect(() => {
    checkServerHealth();
  }, []);

  const checkServerHealth = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/health');
      if (response.ok) {
        setConnectionStatus('connected');
        // Add welcome message
        setMessages([
          {
            role: 'assistant',
            content: "Hello! I'm your AI assistant. How can I help you today?",
            timestamp: new Date().toISOString()
          }
        ]);
      } else {
        setConnectionStatus('error');
      }
    } catch (error) {
      setConnectionStatus('error');
      setError('Unable to connect to the server. Please make sure the backend is running.');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const trimmedMessage = inputMessage.trim();
    
    // Validation
    if (!trimmedMessage) {
      return;
    }

    if (trimmedMessage.length > 4000) {
      setError('Message is too long. Please keep it under 4000 characters.');
      return;
    }

    // Clear any previous errors
    setError(null);

    // Add user message to chat
    const userMessage = {
      role: 'user',
      content: trimmedMessage,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      // Prepare conversation history (exclude system messages and timestamps)
      const conversationHistory = messages
        .filter(msg => msg.role !== 'system')
        .map(msg => ({
          role: msg.role,
          content: msg.content
        }));

      // Send request to backend
      const response = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: trimmedMessage,
          conversationHistory: conversationHistory
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'An error occurred while processing your request');
      }

      // Add AI response to chat
      const assistantMessage = {
        role: 'assistant',
        content: data.message,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, assistantMessage]);

    } catch (error) {
      console.error('Chat error:', error);
      setError(error.message || 'Failed to get response. Please try again.');
      
      // Add error message to chat
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: '❌ Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
        isError: true
      }]);
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const clearChat = () => {
    setMessages([
      {
        role: 'assistant',
        content: "Chat cleared! How can I help you?",
        timestamp: new Date().toISOString()
      }
    ]);
    setError(null);
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <div className="header-content">
          <div className="header-title">
            <h1>🤖 AI ChatBot</h1>
            <span className={`status-indicator ${connectionStatus}`}>
              {connectionStatus === 'connected' ? '● Connected' : 
               connectionStatus === 'error' ? '● Disconnected' : '● Connecting...'}
            </span>
          </div>
          <button 
            className="clear-button" 
            onClick={clearChat}
            disabled={messages.length === 0}
          >
            Clear Chat
          </button>
        </div>
      </div>

      {error && (
        <div className="error-banner">
          <span>⚠️ {error}</span>
          <button onClick={() => setError(null)}>✕</button>
        </div>
      )}

      <div className="messages-container">
        {messages.map((message, index) => (
          <div 
            key={index} 
            className={`message ${message.role} ${message.isError ? 'error-message' : ''}`}
          >
            <div className="message-content">
              <div className="message-header">
                <span className="message-role">
                  {message.role === 'user' ? '👤 You' : '🤖 AI Assistant'}
                </span>
                <span className="message-time">
                  {formatTime(message.timestamp)}
                </span>
              </div>
              <div className="message-text">
                {message.content}
              </div>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="message assistant">
            <div className="message-content">
              <div className="message-header">
                <span className="message-role">🤖 AI Assistant</span>
              </div>
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      <form className="input-container" onSubmit={handleSubmit}>
        <textarea
          ref={inputRef}
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message... (Press Enter to send, Shift+Enter for new line)"
          disabled={isLoading || connectionStatus === 'error'}
          rows="1"
          maxLength="4000"
        />
        <button 
          type="submit" 
          disabled={!inputMessage.trim() || isLoading || connectionStatus === 'error'}
          className="send-button"
        >
          {isLoading ? '⏳' : '📤'}
        </button>
      </form>

      <div className="input-footer">
        <span className="character-count">
          {inputMessage.length} / 4000
        </span>
      </div>
    </div>
  );
};

export default ChatBot;

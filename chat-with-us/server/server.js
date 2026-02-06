const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// Security middleware
app.use(helmet());
app.use(cors());
app.use(express.json({ limit: '10mb' }));

// Rate limiting to prevent abuse
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.'
});
app.use('/api/', limiter);

// OpenAI API key from environment variable
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

// Validate API key exists
if (!OPENAI_API_KEY) {
  console.error('ERROR: OPENAI_API_KEY is not set in environment variables');
  process.exit(1);
}

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', message: 'Server is running' });
});

// Chat endpoint
app.post('/api/chat', async (req, res) => {
  try {
    const { message, conversationHistory = [] } = req.body;

    // Input validation
    if (!message || typeof message !== 'string') {
      return res.status(400).json({ 
        error: 'Invalid input', 
        message: 'Message is required and must be a string' 
      });
    }

    if (message.trim().length === 0) {
      return res.status(400).json({ 
        error: 'Invalid input', 
        message: 'Message cannot be empty' 
      });
    }

    if (message.length > 4000) {
      return res.status(400).json({ 
        error: 'Invalid input', 
        message: 'Message is too long. Please keep it under 4000 characters' 
      });
    }

    // Validate conversation history
    if (!Array.isArray(conversationHistory)) {
      return res.status(400).json({ 
        error: 'Invalid input', 
        message: 'Conversation history must be an array' 
      });
    }

    // Build messages array for OpenAI API
    const messages = [
      {
        role: 'system',
        content: 'You are a helpful, friendly, and knowledgeable AI assistant. Provide clear, accurate, and contextually relevant responses. Be concise but thorough, and maintain a conversational tone.'
      },
      ...conversationHistory.slice(-10), // Keep last 10 messages for context
      {
        role: 'user',
        content: message
      }
    ];

    // Call OpenAI API
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${OPENAI_API_KEY}`
      },
      body: JSON.stringify({
        model: 'gpt-3.5-turbo',
        messages: messages,
        max_tokens: 1000,
        temperature: 0.7,
        top_p: 1,
        frequency_penalty: 0,
        presence_penalty: 0
      })
    });

    const data = await response.json();

    // Handle API errors
    if (!response.ok) {
      console.error('OpenAI API Error:', data);
      
      if (response.status === 401) {
        return res.status(401).json({ 
          error: 'Authentication failed', 
          message: 'Invalid or expired API key' 
        });
      }
      
      if (response.status === 429) {
        return res.status(429).json({ 
          error: 'Rate limit exceeded', 
          message: 'Too many requests. Please try again in a moment' 
        });
      }
      
      if (response.status === 500) {
        return res.status(500).json({ 
          error: 'OpenAI service error', 
          message: 'The AI service is temporarily unavailable. Please try again' 
        });
      }

      return res.status(response.status).json({ 
        error: 'API error', 
        message: data.error?.message || 'An error occurred while processing your request' 
      });
    }

    // Extract and send response
    const aiMessage = data.choices[0]?.message?.content;
    
    if (!aiMessage) {
      return res.status(500).json({ 
        error: 'Invalid response', 
        message: 'Received an invalid response from the AI service' 
      });
    }

    res.json({ 
      message: aiMessage,
      success: true,
      usage: data.usage
    });

  } catch (error) {
    console.error('Server Error:', error);
    
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
      return res.status(503).json({ 
        error: 'Connection error', 
        message: 'Unable to connect to the AI service. Please check your internet connection' 
      });
    }

    res.status(500).json({ 
      error: 'Server error', 
      message: 'An unexpected error occurred. Please try again' 
    });
  }
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Not found', message: 'Endpoint not found' });
});

// Start server
app.listen(PORT, () => {
  console.log(`✅ Server is running on port ${PORT}`);
  console.log(`✅ API key is configured`);
  console.log(`📡 Health check: http://localhost:${PORT}/api/health`);
});

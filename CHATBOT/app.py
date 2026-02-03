"""
APS Naturals Chatbot - Web Interface
Knowledge-based chatbot that dynamically generates answers
"""

from flask import Flask, render_template, request, jsonify
import os
import random
from knowledge_base import get_knowledge_base
from preprocessing import clean_text

app = Flask(__name__)

# Load knowledge base
print("="*60)
print("🚀 APS Naturals Chatbot - Web Server")
print("="*60)

try:
    print("\n📚 Loading knowledge base...")
    kb = get_knowledge_base()
    kb_loaded = True
    print(f"✅ Knowledge base loaded successfully!")
    print(f"   - {len(kb.all_sentences)} information pieces")
    print(f"   - {len(kb.sections)} categories")
except Exception as e:
    print(f"❌ Error loading knowledge base: {e}")
    kb_loaded = False

# Predefined conversation starters and follow-up suggestions
CONVERSATION_STARTERS = [
    "What is APS Naturals?",
    "What products do you offer?",
    "Are your products organic?",
    "Tell me about your sustainability practices",
    "What makes APS Naturals different?",
    "Are your products cruelty-free?",
    "Can I use APS products for sensitive skin?",
    "What values does APS Naturals promote?"
]

TOPIC_SUGGESTIONS = {
    "products": [
        "What types of products does APS Naturals offer?",
        "Are APS products safe for daily use?",
        "Tell me about your organic products"
    ],
    "quality": [
        "How do you ensure product quality?",
        "Do you use harmful chemicals?",
        "Are your products cruelty-free?"
    ],
    "sustainability": [
        "Are APS products eco-friendly?",
        "What are your sustainability practices?",
        "How do you protect the environment?"
    ],
    "usage": [
        "Who can use APS products?",
        "Are products suitable for all ages?",
        "Can I use products on sensitive skin?"
    ],
    "company": [
        "What is APS Naturals' mission?",
        "What values does APS Naturals promote?",
        "What makes APS Naturals different?"
    ]
}

def get_topic_from_query(query):
    """Identify the topic of a query"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ["product", "offer", "type", "sell", "have"]):
        return "products"
    elif any(word in query_lower for word in ["quality", "safe", "chemical", "test", "cruelty"]):
        return "quality"
    elif any(word in query_lower for word in ["eco", "environment", "sustain", "green", "nature"]):
        return "sustainability"
    elif any(word in query_lower for word in ["use", "who", "age", "skin", "daily", "apply"]):
        return "usage"
    elif any(word in query_lower for word in ["mission", "value", "company", "brand", "different", "about"]):
        return "company"
    else:
        return "company"

def get_follow_up_suggestions(user_query):
    """Generate relevant follow-up questions"""
    topic = get_topic_from_query(user_query)
    
    # Get suggestions from identified topic
    suggestions = TOPIC_SUGGESTIONS.get(topic, TOPIC_SUGGESTIONS["company"]).copy()
    
    # Add one from a different topic
    other_topics = [t for t in TOPIC_SUGGESTIONS.keys() if t != topic]
    if other_topics:
        random_topic = random.choice(other_topics)
        suggestions.append(random.choice(TOPIC_SUGGESTIONS[random_topic]))
    
    # Shuffle and limit
    random.shuffle(suggestions)
    return suggestions[:4]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not kb_loaded:
        return jsonify({
            'response': "❌ Knowledge base is not loaded. Please check the server logs.",
            'suggestions': [],
            'error': True
        })
    
    try:
        user_message = request.json.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'response': "Please ask me a question about APS Naturals.",
                'suggestions': random.sample(CONVERSATION_STARTERS, 4)
            })
        
        # Clean input
        cleaned_input = clean_text(user_message)
        
        if not cleaned_input:
            return jsonify({
                'response': "I didn't quite understand that. Could you rephrase your question?",
                'suggestions': get_follow_up_suggestions(user_message)
            })
        
        # Generate answer from knowledge base
        answer, confidence = kb.generate_answer(user_message)
        
        if answer and confidence > 0.12:
            response = answer
            suggestions = get_follow_up_suggestions(user_message)
        else:
            response = ("I don't have specific information about that. "
                       "I can answer questions about APS Naturals products, "
                       "quality standards, sustainability practices, and company values.")
            suggestions = random.sample(CONVERSATION_STARTERS, 4)
        
        return jsonify({
            'response': response,
            'suggestions': suggestions,
            'confidence': float(confidence) if confidence else 0.0
        })
    
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({
            'response': "An error occurred while processing your question. Please try again.",
            'suggestions': random.sample(CONVERSATION_STARTERS, 4),
            'error': True
        })

@app.route('/initial-suggestions', methods=['GET'])
def initial_suggestions():
    """Provide initial conversation starters"""
    return jsonify({'suggestions': random.sample(CONVERSATION_STARTERS, 4)})

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'kb_loaded': kb_loaded,
        'knowledge_pieces': len(kb.all_sentences) if kb_loaded else 0
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    if kb_loaded:
        print("✅ Server ready!")
        print("📱 Open your browser: http://localhost:5000")
        print("💬 Knowledge-based chatbot is active")
    else:
        print("⚠️  Knowledge base not loaded")
        print("📱 Server will start but chatbot won't work properly")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

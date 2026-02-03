"""
APS Naturals AI Chatbot - Console Interface
This chatbot uses a knowledge base to dynamically generate answers
to questions about APS Naturals products, values, and services.
"""

import sys
import os
from knowledge_base import get_knowledge_base
from preprocessing import clean_text

print("="*60)
print("🤖 APS Naturals AI Chatbot - Knowledge-Based System")
print("="*60)

# Load knowledge base
print("\n📚 Loading knowledge base...")
try:
    kb = get_knowledge_base()
    print(f"✅ Knowledge base loaded successfully!")
    print(f"   - {len(kb.all_sentences)} information pieces available")
    print(f"   - {len(kb.sections)} categories indexed")
except Exception as e:
    print(f"❌ Error loading knowledge base: {e}")
    sys.exit(1)

def chatbot_response(user_input):
    """Generate dynamic response based on knowledge base search"""
    try:
        # Clean the input
        cleaned_input = clean_text(user_input)
        
        if not cleaned_input:
            return "I didn't understand that. Could you please rephrase your question?"
        
        # Generate answer from knowledge base
        answer, confidence = kb.generate_answer(user_input)
        
        if answer and confidence > 0.15:
            return answer
        else:
            # Provide helpful fallback
            return ("I don't have specific information about that. "
                   "I can answer questions about APS Naturals products, "
                   "quality standards, sustainability practices, and company values.")
    
    except Exception as e:
        return f"Error processing your question: {str(e)}"

print("\n✅ Chatbot is ready!")
print("💬 Ask me anything about APS Naturals")
print("🛑 Type 'exit', 'quit', or 'bye' to stop\n")
print("-"*60 + "\n")

while True:
    try:
        user = input("You: ").strip()
        
        if not user:
            continue
            
        if user.lower() in ['exit', 'quit', 'bye', 'goodbye']:
            print("\nBot: Thank you for using APS Naturals chatbot! Have a great day! 👋\n")
            break
        
        response = chatbot_response(user)
        print(f"\nBot: {response}\n")
        print("-"*60 + "\n")
        
    except KeyboardInterrupt:
        print("\n\nBot: Goodbye! Thanks for chatting! 👋\n")
        break
    except Exception as e:
        print(f"\nAn error occurred: {e}\n")
        break


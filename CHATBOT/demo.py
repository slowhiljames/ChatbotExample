"""
Quick Demo - Test the Knowledge-Based Chatbot
This script demonstrates how the new chatbot answers various questions
"""

from knowledge_base import get_knowledge_base

print("="*70)
print("APS NATURALS CHATBOT - DEMO")
print("="*70)

# Load knowledge base
kb = get_knowledge_base()

# Test questions - various formats
test_questions = [
    "What is APS Naturals?",
    "Tell me about your products",
    "Do you use harmful chemicals?",
    "Are your products eco-friendly?",
    "Can I use these for sensitive skin?",
    "What makes you different?",
    "Is it organic?",
    "Who can use your products?",
    "Tell me about sustainability",
    "How do you ensure quality?"
]

print("\n🧪 Testing different question formats:\n")
print("="*70)

for question in test_questions:
    answer, confidence = kb.generate_answer(question)
    print(f"\n❓ Question: {question}")
    print(f"💬 Answer: {answer}")
    print(f"📊 Confidence: {confidence:.2%}")
    print("-"*70)

print("\n✅ Demo completed!")
print("="*70)
print("\nNOTICE: The chatbot generates different answers based on context!")
print("Try running: python chatbot.py for interactive testing")
print("="*70)

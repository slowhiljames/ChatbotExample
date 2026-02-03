"""
APS Naturals Chatbot - Setup and Verification Script

NOTE: This chatbot now uses a knowledge-based approach instead of neural network training.
This script verifies that all required components are in place.
"""

import os
import sys

print("="*70)
print("APS Naturals Chatbot - Knowledge-Based System Setup")
print("="*70)

# Check if dataset exists
print("\n📂 Checking knowledge base file...")
if not os.path.exists("dataset/apsnaturals_qa_dataset.txt"):
    print("❌ Error: Knowledge base file not found!")
    print("   Expected: dataset/apsnaturals_qa_dataset.txt")
    sys.exit(1)

print("✅ Knowledge base file found")

# Verify knowledge base can be loaded
print("\n🔍 Verifying knowledge base structure...")
try:
    from knowledge_base import get_knowledge_base
    kb = get_knowledge_base()
    print(f"✅ Knowledge base loaded successfully!")
    print(f"   - {len(kb.all_sentences)} information pieces")
    print(f"   - {len(kb.sections)} categories:")
    for section in kb.sections.keys():
        print(f"      • {section}")
except Exception as e:
    print(f"❌ Error loading knowledge base: {e}")
    sys.exit(1)

# Test the chatbot response system
print("\n🧪 Testing chatbot response generation...")
try:
    test_questions = [
        "What is APS Naturals?",
        "Are your products organic?",
        "Tell me about sustainability"
    ]
    
    for question in test_questions:
        answer, confidence = kb.generate_answer(question)
        if answer:
            print(f"✅ Test passed: '{question[:40]}...'")
        else:
            print(f"⚠️  Low confidence for: '{question}'")
            
except Exception as e:
    print(f"❌ Error testing chatbot: {e}")
    sys.exit(1)

# Check if required dependencies are installed
print("\n📦 Checking dependencies...")
try:
    import flask
    print("✅ Flask installed")
except ImportError:
    print("⚠️  Flask not installed. Install with: pip install flask")

try:
    import sklearn
    print("✅ scikit-learn installed")
except ImportError:
    print("⚠️  scikit-learn not installed. Install with: pip install scikit-learn")

try:
    import nltk
    print("✅ NLTK installed")
except ImportError:
    print("⚠️  NLTK not installed. Install with: pip install nltk")

print("\n" + "="*70)
print("✅ Setup verification completed!")
print("="*70)
print("\n📋 Next Steps:")
print("   1. Run console chatbot: python chatbot.py")
print("   2. Run web interface:   python app.py")
print("   3. Then open browser:   http://localhost:5000")
print("\n💡 Note: This chatbot uses knowledge-based retrieval.")
print("   No training is needed - it dynamically generates answers!")
print("="*70 + "\n")


"""
Interactive Test - See how the chatbot answers your questions!
This demonstrates the knowledge-based system in action.
"""

from knowledge_base import get_knowledge_base

print("╔" + "═"*70 + "╗")
print("║" + " "*70 + "║")
print("║" + "  🤖 APS NATURALS KNOWLEDGE-BASED CHATBOT - INTERACTIVE TEST".center(70) + "║")
print("║" + " "*70 + "║")
print("╚" + "═"*70 + "╝")

# Load knowledge base
kb = get_knowledge_base()

print("\n✅ Knowledge Base Loaded:")
print(f"   • {len(kb.all_sentences)} information pieces")
print(f"   • {len(kb.sections)} knowledge categories")

print("\n" + "─"*70)
print("\n💡 Ask me anything about APS Naturals!")
print("   Type 'quit', 'exit', or 'bye' to stop\n")
print("─"*70 + "\n")

while True:
    try:
        question = input("You: ").strip()
        
        if not question:
            continue
        
        if question.lower() in ['quit', 'exit', 'bye', 'goodbye']:
            print("\n✨ Thanks for testing the chatbot! Have a great day!\n")
            break
        
        # Get answer
        answer, confidence = kb.generate_answer(question)
        
        if answer and confidence > 0.12:
            print(f"\n🤖 Bot: {answer}")
            print(f"   📊 Confidence: {confidence:.1%}\n")
        else:
            print(f"\n🤖 Bot: I don't have specific information about that.")
            print(f"   💡 Try asking about products, quality, sustainability, or values.\n")
        
        print("─"*70 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n✨ Goodbye!\n")
        break
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        break

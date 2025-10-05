#!/usr/bin/env python3
"""
Test script to check what the RAG database is returning
"""

from services.rag_database import RAGDatabase

def test_rag_database():
    """Test the RAG database directly"""
    print("🧠 Testing RAG Database")
    print("=" * 50)
    
    # Create RAG database
    rag_db = RAGDatabase()
    
    # Test context
    context = "This collection features white, with, close, photo, blue. The collection contains 5 photos."
    photo_count = 5
    
    print(f"Context: {context}")
    print(f"Photo count: {photo_count}")
    print()
    
    # Test effects
    print("1. Testing effects...")
    effects = rag_db.get_relevant_effects(context, photo_count)
    print(f"Effects returned: {len(effects)}")
    for i, effect in enumerate(effects):
        print(f"  {i+1}. {effect['name']} - {effect['description']}")
    print()
    
    # Test transitions
    print("2. Testing transitions...")
    transitions = rag_db.get_relevant_transitions(context, photo_count)
    print(f"Transitions returned: {len(transitions)}")
    for i, transition in enumerate(transitions):
        print(f"  {i+1}. {transition['name']} - {transition['description']}")
    print()
    
    # Test music
    print("3. Testing music...")
    music = rag_db.get_relevant_music(context)
    print(f"Music style: {music['name']} - {music['description']}")
    print()
    
    # Test template
    print("4. Testing template...")
    template = rag_db.get_relevant_template(context)
    print(f"Template: {template['name']} - {template['description']}")
    print(f"Template effects: {template['effects']}")
    print(f"Template transitions: {template['transitions']}")
    print()
    
    # Test complete RAG context
    print("5. Testing complete RAG context...")
    rag_context = rag_db.get_rag_context(context, photo_count)
    print(f"RAG context keys: {list(rag_context.keys())}")
    print(f"Effects in RAG context: {[effect['name'] for effect in rag_context['effects']]}")
    print(f"Transitions in RAG context: {[transition['name'] for transition in rag_context['transitions']]}")
    print(f"Music in RAG context: {rag_context['music_style']['name']}")
    print()
    
    print("=" * 50)
    print("🎉 RAG database test completed!")

if __name__ == "__main__":
    test_rag_database()

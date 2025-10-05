#!/usr/bin/env python3
"""
Test script to check what the RAG Gemini service is returning
"""

from services.rag_gemini_service import RAGGeminiService

def test_rag_gemini():
    """Test the RAG Gemini service directly"""
    print("🤖 Testing RAG Gemini Service")
    print("=" * 50)
    
    # Create RAG Gemini service
    rag_gemini = RAGGeminiService()
    
    # Test data
    photo_paths = ["test1.jpg", "test2.jpg", "test3.jpg", "test4.jpg", "test5.jpg"]
    context = "This collection features white, with, close, photo, blue. The collection contains 5 photos."
    
    print(f"Photo paths: {photo_paths}")
    print(f"Context: {context}")
    print()
    
    # Test RAG planning
    print("1. Testing RAG video planning...")
    try:
        video_plan = rag_gemini.plan_video_with_rag(photo_paths, context)
        print(f"Video plan returned: {video_plan}")
        print()
        
        print("Video plan details:")
        print(f"  - Sequence: {video_plan.get('sequence', [])}")
        print(f"  - Effects: {video_plan.get('effects', [])}")
        print(f"  - Transitions: {video_plan.get('transitions', [])}")
        print(f"  - Music style: {video_plan.get('music_style', '')}")
        print(f"  - Duration per photo: {video_plan.get('duration_per_photo', 0)}")
        print(f"  - Video style: {video_plan.get('video_style', '')}")
        print(f"  - Mood: {video_plan.get('mood', '')}")
        
    except Exception as e:
        print(f"Error in RAG planning: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 50)
    print("🎉 RAG Gemini service test completed!")

if __name__ == "__main__":
    test_rag_gemini()

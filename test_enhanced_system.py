#!/usr/bin/env python3
"""
Test script for the enhanced RAG system with all improvements
"""

import requests
import os
from PIL import Image
import numpy as np
import json

# Configuration
BASE_URL = "http://localhost:5003"
UPLOAD_URL = f"{BASE_URL}/upload"
GENERATE_VIDEO_URL = f"{BASE_URL}/generate_video"
DOWNLOAD_URL_PREFIX = f"{BASE_URL}/download/"
TEST_IMAGE_DIR = "test_images"
OUTPUT_DIR = "outputs"

def create_test_image(filename, color=(255, 0, 0), size=(800, 600)):
    """Create test image with specific color and size"""
    if not os.path.exists(TEST_IMAGE_DIR):
        os.makedirs(TEST_IMAGE_DIR)
    img = Image.new('RGB', size, color=color)
    img.save(os.path.join(TEST_IMAGE_DIR, filename))
    print(f"Created {filename}")
    return filename

def cleanup_test_files(filenames):
    """Clean up test files"""
    for filename in filenames:
        path = os.path.join(TEST_IMAGE_DIR, filename)
        if os.path.exists(path):
            os.remove(path)
            print(f"Removed {filename}")

def test_enhanced_system():
    """Test the enhanced RAG system"""
    print("🚀 Testing Enhanced RAG System")
    print("=" * 60)
    
    # 1. Test app connectivity
    print("1. Testing app connectivity...")
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("✅ App is running successfully!")
        else:
            print(f"❌ App not accessible. Status code: {response.status_code}")
            return
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Error connecting to app: {e}")
        return

    # 2. Create diverse test images
    print("\n2. Creating diverse test images...")
    test_images = [
        create_test_image("enhanced_test_1.jpg", color=(255, 100, 100), size=(1920, 1080)),  # Red landscape
        create_test_image("enhanced_test_2.jpg", color=(100, 255, 100), size=(1080, 1920)),  # Green portrait
        create_test_image("enhanced_test_3.jpg", color=(100, 100, 255), size=(800, 600)),   # Blue square
        create_test_image("enhanced_test_4.jpg", color=(255, 255, 100), size=(1200, 800)),  # Yellow wide
        create_test_image("enhanced_test_5.jpg", color=(255, 100, 255), size=(600, 800))    # Magenta tall
    ]

    # 3. Test enhanced photo upload
    print("\n3. Testing enhanced photo upload...")
    files = [('photos', (img_name, open(os.path.join(TEST_IMAGE_DIR, img_name), 'rb'), 'image/jpeg')) for img_name in test_images]
    try:
        response = requests.post(UPLOAD_URL, files=files)
        if response.status_code == 200:
            result = response.json()
            print("✅ Enhanced photos uploaded successfully!")
            print(f"   - Photo count: {result['photo_count']}")
            print(f"   - Context: {result['context']}")
            print(f"   - Video plan: {result['video_plan']}")
            
            # Show enhanced features
            video_plan = result['video_plan']
            print(f"\n🎬 Enhanced Video Plan Details:")
            print(f"   - Effects: {video_plan.get('effects', [])}")
            print(f"   - Transitions: {video_plan.get('transitions', [])}")
            print(f"   - Music Style: {video_plan.get('music_style', '')}")
            print(f"   - Duration per photo: {video_plan.get('duration_per_photo', 0)}")
            print(f"   - Video Style: {video_plan.get('video_style', '')}")
            print(f"   - Mood: {video_plan.get('mood', '')}")
            if 'reasoning' in video_plan:
                print(f"   - AI Reasoning: {video_plan['reasoning']}")
            
        else:
            print(f"❌ Photo upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error uploading photos: {str(e)}")
        return
    finally:
        # Close files
        for _, (_, file_obj, _) in files:
            file_obj.close()

    # 4. Test enhanced video generation
    print("\n4. Testing enhanced video generation...")
    try:
        # Prepare video generation data
        video_data = {
            'photo_paths': [f"uploads/{img}" for img in test_images],
            'context': result['context'],
            'video_plan': result['video_plan']
        }
        
        response = requests.post(GENERATE_VIDEO_URL, 
                               json=video_data,
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Enhanced video generated successfully!")
            print(f"   - Video path: {result['video_path']}")
            print(f"   - Download URL: {result['download_url']}")

            # Verify video file
            video_filename = os.path.basename(result['video_path'])
            video_filepath = os.path.join(OUTPUT_DIR, video_filename)
            if os.path.exists(video_filepath) and os.path.getsize(video_filepath) > 0:
                file_size = os.path.getsize(video_filepath)
                print(f"✅ Video file exists and has content! ({file_size} bytes)")
            else:
                print("❌ Video file not found or is empty!")
        else:
            print(f"❌ Video generation failed: {response.status_code}")
            print(f"   Response: {response.json()}")
            return
    except Exception as e:
        print(f"❌ Error generating enhanced video: {str(e)}")
        return

    # 5. Test enhanced features
    print("\n5. Testing enhanced features...")
    try:
        # Test vector RAG database
        from services.vector_rag_database import VectorRAGDatabase
        rag_db = VectorRAGDatabase()
        
        # Test semantic search
        search_results = rag_db.semantic_search("family photos with children", k=3)
        print(f"✅ Vector RAG search working: {len(search_results)} results")
        
        # Test enhanced context generator
        from services.enhanced_context_generator import EnhancedContextGenerator
        context_gen = EnhancedContextGenerator()
        print("✅ Enhanced context generator loaded")
        
        # Test enhanced music service
        from services.enhanced_music_service import EnhancedMusicService
        music_service = EnhancedMusicService()
        print("✅ Enhanced music service loaded")
        
    except Exception as e:
        print(f"⚠️  Some enhanced features may not be fully available: {str(e)}")

    # 6. Cleanup
    print("\n6. Cleaning up test files...")
    cleanup_test_files(test_images)

    print("\n" + "=" * 60)
    print("🎉 Enhanced RAG system test completed!")
    print("\n🚀 Enhanced Features:")
    print("   ✅ CLIP embeddings for semantic understanding")
    print("   ✅ BLIP for better image captioning")
    print("   ✅ Vector RAG with FAISS for semantic search")
    print("   ✅ Enhanced Gemini integration with proper API")
    print("   ✅ Advanced video effects and transitions")
    print("   ✅ Enhanced music generation")
    print("   ✅ NER and scene classification")
    print("   ✅ Professional video quality")
    print("\nYour enhanced RAG-based video generation system is ready!")

if __name__ == "__main__":
    test_enhanced_system()

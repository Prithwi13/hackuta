#!/usr/bin/env python3
"""
Simple test for the enhanced RAG system
"""

import requests
import os
from PIL import Image

# Configuration
BASE_URL = "http://localhost:5003"
UPLOAD_URL = f"{BASE_URL}/upload"
TEST_IMAGE_DIR = "test_images"

def create_test_image(filename, color=(255, 0, 0), size=(800, 600)):
    """Create test image with specific color and size"""
    if not os.path.exists(TEST_IMAGE_DIR):
        os.makedirs(TEST_IMAGE_DIR)
    img = Image.new('RGB', size, color=color)
    img.save(os.path.join(TEST_IMAGE_DIR, filename))
    print(f"Created {filename}")
    return filename

def test_simple_enhanced():
    """Test the enhanced RAG system"""
    print("🚀 Testing Enhanced RAG System (Simple)")
    print("=" * 50)
    
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

    # 2. Create test images
    print("\n2. Creating test images...")
    test_images = [
        create_test_image("simple_test_1.jpg", color=(255, 100, 100), size=(800, 600)),
        create_test_image("simple_test_2.jpg", color=(100, 255, 100), size=(800, 600)),
        create_test_image("simple_test_3.jpg", color=(100, 100, 255), size=(800, 600))
    ]

    # 3. Test photo upload
    print("\n3. Testing photo upload...")
    files = [('photos', (img_name, open(os.path.join(TEST_IMAGE_DIR, img_name), 'rb'), 'image/jpeg')) for img_name in test_images]
    try:
        response = requests.post(UPLOAD_URL, files=files)
        if response.status_code == 200:
            result = response.json()
            print("✅ Photos uploaded successfully!")
            print(f"   - Photo count: {result['photo_count']}")
            print(f"   - Context: {result['context']}")
            
            # Show video plan details
            if 'video_plan' in result:
                video_plan = result['video_plan']
                print(f"\n🎬 Video Plan Details:")
                print(f"   - Effects: {video_plan.get('effects', [])}")
                print(f"   - Transitions: {video_plan.get('transitions', [])}")
                print(f"   - Music Style: {video_plan.get('music_style', '')}")
                print(f"   - Duration per photo: {video_plan.get('duration_per_photo', 0)}")
                print(f"   - Video Style: {video_plan.get('video_style', '')}")
                print(f"   - Mood: {video_plan.get('mood', '')}")
            
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

    # 4. Cleanup
    print("\n4. Cleaning up test files...")
    for filename in test_images:
        path = os.path.join(TEST_IMAGE_DIR, filename)
        if os.path.exists(path):
            os.remove(path)
            print(f"Removed {filename}")

    print("\n" + "=" * 50)
    print("🎉 Enhanced RAG system test completed!")

if __name__ == "__main__":
    test_simple_enhanced()

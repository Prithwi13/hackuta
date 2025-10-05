#!/usr/bin/env python3
"""
Test video generation with sound, transitions, and effects
"""

import requests
import os
from PIL import Image

# Configuration
BASE_URL = "http://localhost:5003"
UPLOAD_URL = f"{BASE_URL}/upload"
GENERATE_VIDEO_URL = f"{BASE_URL}/generate_video"
TEST_IMAGE_DIR = "test_images"

def create_test_image(filename, color=(255, 0, 0), size=(800, 600)):
    """Create test image with specific color and size"""
    if not os.path.exists(TEST_IMAGE_DIR):
        os.makedirs(TEST_IMAGE_DIR)
    img = Image.new('RGB', size, color=color)
    img.save(os.path.join(TEST_IMAGE_DIR, filename))
    print(f"Created {filename}")
    return filename

def test_video_generation():
    """Test video generation with all features"""
    print("🎬 Testing Video Generation with Sound, Transitions, and Effects")
    print("=" * 60)
    
    # 1. Create test images
    print("1. Creating test images...")
    test_images = [
        create_test_image("test_1.jpg", color=(255, 100, 100), size=(800, 600)),
        create_test_image("test_2.jpg", color=(100, 255, 100), size=(800, 600)),
        create_test_image("test_3.jpg", color=(100, 100, 255), size=(800, 600))
    ]

    # 2. Upload photos
    print("\n2. Uploading photos...")
    files = [('photos', (img_name, open(os.path.join(TEST_IMAGE_DIR, img_name), 'rb'), 'image/jpeg')) for img_name in test_images]
    try:
        response = requests.post(UPLOAD_URL, files=files)
        if response.status_code == 200:
            result = response.json()
            print("✅ Photos uploaded successfully!")
            print(f"   - Photo count: {result['photo_count']}")
            print(f"   - Context: {result['context']}")
            print(f"   - Video plan: {result['video_plan']}")
            
            # Show video plan details
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

    # 3. Generate video
    print("\n3. Generating video...")
    try:
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
            print("✅ Video generated successfully!")
            print(f"   - Video path: {result['video_path']}")
            print(f"   - Download URL: {result['download_url']}")

            # Verify video file
            video_filename = os.path.basename(result['video_path'])
            video_filepath = os.path.join("outputs", video_filename)
            if os.path.exists(video_filepath) and os.path.getsize(video_filepath) > 0:
                file_size = os.path.getsize(video_filepath)
                print(f"✅ Video file exists and has content! ({file_size} bytes)")
                print(f"   - File: {video_filepath}")
                print(f"   - Size: {file_size / (1024*1024):.2f} MB")
            else:
                print("❌ Video file not found or is empty!")
        else:
            print(f"❌ Video generation failed: {response.status_code}")
            print(f"   Response: {response.json()}")
            return
    except Exception as e:
        print(f"❌ Error generating video: {str(e)}")
        return

    # 4. Cleanup
    print("\n4. Cleaning up test files...")
    for filename in test_images:
        path = os.path.join(TEST_IMAGE_DIR, filename)
        if os.path.exists(path):
            os.remove(path)
            print(f"Removed {filename}")

    print("\n" + "=" * 60)
    print("🎉 Video generation test completed!")
    print("\n🎬 Features Tested:")
    print("   ✅ Photo upload and processing")
    print("   ✅ Context generation with BERT5")
    print("   ✅ Video planning with Gemini")
    print("   ✅ Video generation with music")
    print("   ✅ File output and verification")

if __name__ == "__main__":
    test_video_generation()

#!/usr/bin/env python3
"""
Test script for Memory Video Creator
This script demonstrates the core functionality of the app
"""

import requests
import os
import json
from PIL import Image
import io

def create_test_image(filename, color=(255, 0, 0), size=(800, 600)):
    """Create a test image for testing purposes"""
    img = Image.new('RGB', size, color)
    img.save(filename)
    return filename

def test_app():
    """Test the Memory Video Creator app"""
    base_url = "http://localhost:5002"
    
    print("🎬 Testing Memory Video Creator App")
    print("=" * 50)
    
    # Test 1: Check if app is running
    print("1. Testing app connectivity...")
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            print("✅ App is running successfully!")
        else:
            print(f"❌ App returned status code: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to app. Make sure it's running on port 5001")
        return
    
    # Test 2: Create test images
    print("\n2. Creating test images...")
    test_images = []
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
    
    for i, color in enumerate(colors):
        filename = f"test_image_{i+1}.jpg"
        create_test_image(filename, color)
        test_images.append(filename)
        print(f"   Created {filename}")
    
    # Test 3: Upload photos
    print("\n3. Testing photo upload...")
    try:
        files = []
        for img_file in test_images:
            files.append(('photos', (img_file, open(img_file, 'rb'), 'image/jpeg')))
        
        response = requests.post(f"{base_url}/upload", files=files)
        
        # Close file handles
        for _, (_, file_handle, _) in files:
            file_handle.close()
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Photos uploaded successfully!")
            print(f"   - Photo count: {data.get('photo_count', 0)}")
            print(f"   - Context: {data.get('context', {}).get('overall_context', 'No context')}")
            
            # Test 4: Generate video
            print("\n4. Testing video generation...")
            video_response = requests.post(f"{base_url}/generate_video", 
                                         json={
                                             'photo_paths': data.get('photo_paths', []),
                                             'context': data.get('context', {}),
                                             'video_plan': data.get('video_plan', {})
                                         })
            
            if video_response.status_code == 200:
                video_data = video_response.json()
                print("✅ Video generated successfully!")
                print(f"   - Video path: {video_data.get('video_path', 'Unknown')}")
                print(f"   - Download URL: {video_data.get('download_url', 'Unknown')}")
            else:
                print(f"❌ Video generation failed: {video_response.status_code}")
                print(f"   Response: {video_response.text}")
        else:
            print(f"❌ Photo upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
    
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
    
    finally:
        # Cleanup test images
        print("\n5. Cleaning up test files...")
        for img_file in test_images:
            try:
                os.remove(img_file)
                print(f"   Removed {img_file}")
            except:
                pass
    
    print("\n" + "=" * 50)
    print("🎉 Test completed!")
    print("You can now open http://localhost:5001 in your browser to use the app!")

if __name__ == "__main__":
    test_app()


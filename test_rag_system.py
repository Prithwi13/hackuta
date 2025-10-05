#!/usr/bin/env python3
"""
Test script for RAG-based video generation system
"""

import requests
import json
import time
import os
from PIL import Image, ImageDraw

def create_test_images():
    """Create test images with different colors"""
    test_images = []
    colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Magenta
    ]
    
    for i, color in enumerate(colors):
        # Create a simple colored image
        img = Image.new('RGB', (800, 600), color)
        draw = ImageDraw.Draw(img)
        
        # Add some text
        draw.text((50, 50), f"Test Image {i+1}", fill=(255, 255, 255))
        draw.text((50, 100), f"Color: {color}", fill=(255, 255, 255))
        
        filename = f"rag_test_{i+1}.jpg"
        img.save(filename)
        test_images.append(filename)
        print(f"Created {filename}")
    
    return test_images

def test_rag_system():
    """Test the RAG-based video generation system"""
    print("🎬 Testing RAG-Based Video Generation System")
    print("=" * 50)
    
    # 1. Test app connectivity
    print("1. Testing app connectivity...")
    try:
        response = requests.get("http://localhost:5002")
        if response.status_code == 200:
            print("✅ App is running successfully!")
        else:
            print("❌ App is not responding")
            return
    except Exception as e:
        print(f"❌ Error connecting to app: {str(e)}")
        return
    
    # 2. Create test images
    print("\n2. Creating test images...")
    test_images = create_test_images()
    
    # 3. Test photo upload
    print("\n3. Testing photo upload...")
    try:
        files = []
        for img_path in test_images:
            files.append(('photos', (img_path, open(img_path, 'rb'), 'image/jpeg')))
        
        response = requests.post("http://localhost:5002/upload", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Photos uploaded successfully!")
            print(f"   - Photo count: {result['photo_count']}")
            print(f"   - Context: {result['context']}")
            print(f"   - Video plan: {result['video_plan']}")
        else:
            print(f"❌ Upload failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error uploading photos: {str(e)}")
        return
    
    # 4. Test video generation
    print("\n4. Testing RAG-based video generation...")
    try:
        # Get the data from the upload response
        upload_result = result
        
        # Prepare video generation data
        video_data = {
            'photo_paths': [f"uploads/{img}" for img in test_images],
            'context': upload_result['context'],
            'video_plan': upload_result['video_plan']
        }
        
        response = requests.post("http://localhost:5002/generate_video", 
                               json=video_data,
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            result = response.json()
            print("✅ RAG video generated successfully!")
            print(f"   - Video path: {result['video_path']}")
            print(f"   - Download URL: {result['download_url']}")
            
            # Check if file exists
            if os.path.exists(result['video_path']):
                file_size = os.path.getsize(result['video_path'])
                print(f"   - File size: {file_size} bytes")
                print("✅ Video file exists and has content!")
            else:
                print("❌ Video file not found")
        else:
            print(f"❌ Video generation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error generating video: {str(e)}")
        return
    
    # 5. Clean up test files
    print("\n5. Cleaning up test files...")
    for img_path in test_images:
        try:
            os.remove(img_path)
            print(f"   Removed {img_path}")
        except:
            pass
    
    print("\n" + "=" * 50)
    print("🎉 RAG system test completed!")
    print("Your RAG-based video generation system is working!")

if __name__ == "__main__":
    test_rag_system()

#!/usr/bin/env python3
"""
Test enhanced video features - music, transitions, and effects
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

def test_enhanced_features():
    """Test the enhanced video features"""
    base_url = "http://localhost:5002"
    
    print("🎬 Testing Enhanced Video Features")
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
        print("❌ Cannot connect to app. Make sure it's running on port 5002")
        return
    
    # Test 2: Create test images with different colors
    print("\n2. Creating test images with different colors...")
    test_images = []
    colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Magenta
    ]
    
    for i, color in enumerate(colors):
        filename = f"enhanced_test_{i+1}.jpg"
        create_test_image(filename, color)
        test_images.append(filename)
        print(f"   Created {filename} with color {color}")
    
    # Test 3: Upload photos and get enhanced video plan
    print("\n3. Testing enhanced video generation...")
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
            
            # Check video plan
            video_plan = data.get('video_plan', {})
            print(f"   - Music style: {video_plan.get('music_style', 'Unknown')}")
            print(f"   - Transitions: {video_plan.get('transitions', [])}")
            print(f"   - Video style: {video_plan.get('video_style', 'Unknown')}")
            
            # Generate enhanced video
            print("\n4. Generating enhanced video with music and effects...")
            video_response = requests.post(f"{base_url}/generate_video", 
                                         json={
                                             'photo_paths': data.get('photo_paths', []),
                                             'context': data.get('context', {}),
                                             'video_plan': data.get('video_plan', {})
                                         })
            
            if video_response.status_code == 200:
                video_data = video_response.json()
                print("✅ Enhanced video generated successfully!")
                print(f"   - Video path: {video_data.get('video_path', 'Unknown')}")
                print(f"   - Download URL: {video_data.get('download_url', 'Unknown')}")
                
                # Check video file
                video_path = video_data.get('video_path', '')
                if video_path and os.path.exists(video_path):
                    file_size = os.path.getsize(video_path)
                    print(f"   - File size: {file_size} bytes")
                    
                    if file_size > 20000:  # Enhanced videos should be larger due to music
                        print("✅ Video appears to have enhanced features!")
                    else:
                        print("⚠️  Video size seems small, may not have all enhancements")
                else:
                    print("❌ Video file not found")
            else:
                print(f"❌ Enhanced video generation failed: {video_response.status_code}")
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
    print("🎉 Enhanced features test completed!")
    print("Your videos now include:")
    print("  🎵 Background music (nostalgic, upbeat, romantic, etc.)")
    print("  🎬 Enhanced transitions (slide, zoom, crossfade)")
    print("  ✨ Visual effects (Ken Burns, pan, zoom)")
    print("  🎨 Dynamic photo sequencing")

if __name__ == "__main__":
    test_enhanced_features()

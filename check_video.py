#!/usr/bin/env python3
"""
Check video file to verify it's not black
"""

import os
import cv2
import numpy as np

def check_video(video_path):
    """Check if video is black or has content"""
    if not os.path.exists(video_path):
        print(f"Video file not found: {video_path}")
        return False
    
    # Get file size
    file_size = os.path.getsize(video_path)
    print(f"Video file size: {file_size} bytes")
    
    if file_size < 1000:  # Less than 1KB is suspicious
        print("❌ Video file is too small, likely corrupted")
        return False
    
    try:
        # Open video with OpenCV
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print("❌ Could not open video file")
            return False
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps if fps > 0 else 0
        
        print(f"Video properties:")
        print(f"  - FPS: {fps}")
        print(f"  - Frame count: {frame_count}")
        print(f"  - Duration: {duration:.2f} seconds")
        
        # Check first few frames
        frames_checked = 0
        non_black_frames = 0
        
        for i in range(min(10, frame_count)):
            ret, frame = cap.read()
            if not ret:
                break
            
            frames_checked += 1
            
            # Check if frame is mostly black
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            mean_brightness = np.mean(gray)
            
            if mean_brightness > 10:  # Not black
                non_black_frames += 1
                print(f"  Frame {i}: brightness = {mean_brightness:.2f}")
            else:
                print(f"  Frame {i}: brightness = {mean_brightness:.2f} (black)")
        
        cap.release()
        
        print(f"\nAnalysis:")
        print(f"  - Frames checked: {frames_checked}")
        print(f"  - Non-black frames: {non_black_frames}")
        
        if non_black_frames > 0:
            print("✅ Video contains content (not black)")
            return True
        else:
            print("❌ Video appears to be black")
            return False
            
    except Exception as e:
        print(f"❌ Error analyzing video: {str(e)}")
        return False

if __name__ == "__main__":
    # Check the latest video
    import glob
    video_files = glob.glob("outputs/memory_video_*.mp4")
    if video_files:
        video_path = max(video_files, key=os.path.getctime)
        print(f"Testing latest video: {video_path}")
    else:
        video_path = "outputs/memory_video_20251004_214523.mp4"
    check_video(video_path)



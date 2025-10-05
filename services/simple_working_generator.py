import os
import moviepy
from moviepy import VideoFileClip, ImageClip, ColorClip, concatenate_videoclips, AudioClip
from PIL import Image
import random
import numpy as np
from datetime import datetime
from config import *

class SimpleWorkingGenerator:
    def __init__(self):
        self.output_folder = OUTPUT_FOLDER
    
    def create_video(self, photo_paths, context, video_plan):
        """
        Create simple working video from photos with basic music
        """
        try:
            print(f"Creating simple working video with {len(photo_paths)} photos")
            print(f"Photo paths: {photo_paths}")
            
            # Get video plan parameters
            sequence = video_plan.get('sequence', list(range(len(photo_paths))))
            duration_per_photo = video_plan.get('duration_per_photo', 3)
            music_style = video_plan.get('music_style', 'nostalgic')
            
            print(f"Video plan: sequence={sequence}, duration={duration_per_photo}, music={music_style}")
            
            # Create simple clips from photos
            clips = []
            for i, photo_idx in enumerate(sequence):
                if photo_idx < len(photo_paths):
                    photo_path = photo_paths[photo_idx]
                    print(f"Processing photo {i+1}/{len(sequence)}: {photo_path}")
                    
                    # Create simple clip
                    clip = self._create_simple_photo_clip(photo_path, duration_per_photo)
                    clips.append(clip)
                    print(f"Created simple clip {i+1} with duration {clip.duration}")
            
            if not clips:
                raise Exception("No valid clips were created")
            
            print(f"Concatenating {len(clips)} clips...")
            # Simple concatenation without complex transitions
            final_video = concatenate_videoclips(clips, method="compose")
            print(f"Final video duration: {final_video.duration}")
            
            # Add simple background music
            final_video = self._add_simple_background_music(final_video, music_style)
            
            # Generate output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"simple_memory_{timestamp}.mp4"
            output_path = os.path.join(self.output_folder, output_filename)
            
            print(f"Writing simple video to: {output_path}")
            # Write video file with basic settings
            final_video.write_videofile(
                output_path,
                fps=24,  # Standard FPS
                codec='libx264',
                audio_codec='aac'
            )
            
            print(f"Simple video created successfully: {output_path}")
            
            # Clean up
            final_video.close()
            for clip in clips:
                clip.close()
            
            return output_path
            
        except Exception as e:
            print(f"Error creating simple video: {str(e)}")
            import traceback
            traceback.print_exc()
            raise e
    
    def _create_simple_photo_clip(self, photo_path, duration):
        """Create a simple video clip from a photo"""
        try:
            print(f"Creating simple clip from: {photo_path}")
            
            # Verify file exists
            if not os.path.exists(photo_path):
                print(f"File does not exist: {photo_path}")
                return self._create_fallback_clip(duration)
            
            # Load and verify image
            with Image.open(photo_path) as img:
                print(f"Image size: {img.size}, mode: {img.mode}")
                if img.size[0] == 0 or img.size[1] == 0:
                    print("Invalid image dimensions")
                    return self._create_fallback_clip(duration)
            
            # Create clip
            clip = ImageClip(photo_path, duration=duration)
            print(f"Original clip size: {clip.size}")
            
            # Simple resize to fit video dimensions
            clip = self._simple_resize_for_video(clip)
            print(f"Resized clip size: {clip.size}")
            
            return clip
            
        except Exception as e:
            print(f"Error creating simple clip from {photo_path}: {str(e)}")
            return self._create_fallback_clip(duration)
    
    def _create_fallback_clip(self, duration):
        """Create a fallback clip when image processing fails"""
        return ColorClip(size=(DEFAULT_VIDEO_WIDTH, DEFAULT_VIDEO_HEIGHT), color=(50, 50, 50), duration=duration)
    
    def _simple_resize_for_video(self, clip):
        """Simple resize clip for video presentation"""
        try:
            # Calculate scaling factor to fit within target dimensions
            scale_w = DEFAULT_VIDEO_WIDTH / clip.w
            scale_h = DEFAULT_VIDEO_HEIGHT / clip.h
            scale = min(scale_w, scale_h)
            
            # Resize maintaining aspect ratio
            new_w = int(clip.w * scale)
            new_h = int(clip.h * scale)
            
            # Use the correct MoviePy resize method
            clip = clip.resized((new_w, new_h))
            
            return clip
            
        except Exception as e:
            print(f"Error resizing clip: {str(e)}")
            return clip
    
    def _add_simple_background_music(self, video, music_style):
        """Add simple background music to video"""
        try:
            print(f"Adding {music_style} simple background music...")
            
            # Generate simple music based on style
            music = self._create_simple_music(music_style, video.duration)
            
            # Set volume using the correct method
            music = music.with_volume_scaled(0.3)  # 30% volume
            
            return video.with_audio(music)
        except Exception as e:
            print(f"Error adding simple background music: {str(e)}")
            return video
    
    def _create_simple_music(self, style, duration):
        """Create simple music based on style"""
        def make_frame(t):
            # Handle both single values and arrays
            if hasattr(t, '__len__') and len(t) > 1:
                # t is an array
                t = t[0] if len(t) > 0 else 0
            
            if style == 'nostalgic':
                # Simple nostalgic melody
                freq1 = 220  # A3
                freq2 = 277  # C#4
                freq3 = 330  # E4
                
                wave1 = np.sin(2 * np.pi * freq1 * t) * 0.3
                wave2 = np.sin(2 * np.pi * freq2 * t) * 0.25
                wave3 = np.sin(2 * np.pi * freq3 * t) * 0.2
                
                return wave1 + wave2 + wave3
                
            elif style == 'upbeat':
                # Simple upbeat melody
                freq1 = 440  # A4
                freq2 = 554  # C#5
                freq3 = 659  # E5
                
                wave1 = np.sin(2 * np.pi * freq1 * t) * 0.3
                wave2 = np.sin(2 * np.pi * freq2 * t) * 0.25
                wave3 = np.sin(2 * np.pi * freq3 * t) * 0.2
                
                return wave1 + wave2 + wave3
                
            elif style == 'romantic':
                # Simple romantic melody
                freq1 = 392  # G4
                freq2 = 494  # B4
                freq3 = 587  # D5
                
                wave1 = np.sin(2 * np.pi * freq1 * t) * 0.3
                wave2 = np.sin(2 * np.pi * freq2 * t) * 0.25
                wave3 = np.sin(2 * np.pi * freq3 * t) * 0.2
                
                return wave1 + wave2 + wave3
                
            elif style == 'energetic':
                # Simple energetic melody
                freq1 = 523  # C5
                freq2 = 659  # E5
                freq3 = 784  # G5
                
                wave1 = np.sin(2 * np.pi * freq1 * t) * 0.3
                wave2 = np.sin(2 * np.pi * freq2 * t) * 0.25
                wave3 = np.sin(2 * np.pi * freq3 * t) * 0.2
                
                return wave1 + wave2 + wave3
                
            else:  # calm
                # Simple calm melody
                freq1 = 220  # A3
                freq2 = 277  # C#4
                freq3 = 330  # E4
                
                wave1 = np.sin(2 * np.pi * freq1 * t) * 0.3
                wave2 = np.sin(2 * np.pi * freq2 * t) * 0.25
                wave3 = np.sin(2 * np.pi * freq3 * t) * 0.2
                
                return wave1 + wave2 + wave3
        
        return AudioClip(make_frame, duration=duration)

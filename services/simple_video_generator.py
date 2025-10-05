import os
import moviepy
from moviepy import VideoFileClip, ImageClip, ColorClip, concatenate_videoclips, AudioClip
from PIL import Image
import random
import numpy as np
from datetime import datetime
from config import *
from services.music_service import MusicService

class SimpleVideoGenerator:
    def __init__(self):
        self.output_folder = OUTPUT_FOLDER
        self.music_service = MusicService()
    
    def create_video(self, photo_paths, context, video_plan):
        """
        Create simple video from photos with basic transitions and music
        """
        try:
            print(f"Creating simple video with {len(photo_paths)} photos")
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
                    
                    clip = self._create_simple_photo_clip(photo_path, duration_per_photo)
                    clips.append(clip)
                    print(f"Created clip {i+1} with duration {clip.duration}")
            
            if not clips:
                raise Exception("No valid clips were created")
            
            print(f"Concatenating {len(clips)} clips...")
            # Concatenate clips
            final_video = concatenate_videoclips(clips, method="compose")
            print(f"Final video duration: {final_video.duration}")
            
            # Add background music
            final_video = self._add_simple_background_music(final_video, music_style)
            
            # Generate output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"memory_video_{timestamp}.mp4"
            output_path = os.path.join(self.output_folder, output_filename)
            
            print(f"Writing video to: {output_path}")
            # Write video file
            final_video.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True
            )
            
            print(f"Video created successfully: {output_path}")
            
            # Clean up
            final_video.close()
            for clip in clips:
                clip.close()
            
            return output_path
            
        except Exception as e:
            print(f"Error creating video: {str(e)}")
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
            clip = self._simple_resize_clip(clip)
            print(f"Resized clip size: {clip.size}")
            
            return clip
            
        except Exception as e:
            print(f"Error creating simple clip from {photo_path}: {str(e)}")
            return self._create_fallback_clip(duration)
    
    def _create_fallback_clip(self, duration):
        """Create a fallback clip when image processing fails"""
        return ColorClip(size=(DEFAULT_VIDEO_WIDTH, DEFAULT_VIDEO_HEIGHT), color=(100, 100, 100), duration=duration)
    
    def _simple_resize_clip(self, clip):
        """Simple resize clip to standard dimensions"""
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
            print(f"Adding {music_style} background music...")
            
            # Generate music based on style
            music = self.music_service.get_background_music(music_style, video.duration)
            
            # Set volume (not too loud)
            music = music.with_volume_scaled(0.3)
            
            return video.with_audio(music)
        except Exception as e:
            print(f"Error adding background music: {str(e)}")
            # Return video without audio if music fails
            return video

import os
import moviepy
from moviepy import VideoFileClip, ImageClip, ColorClip, concatenate_videoclips, AudioClip, CompositeVideoClip
from PIL import Image
import random
import numpy as np
from datetime import datetime
from config import *

class EnhancedWorkingGenerator:
    def __init__(self):
        self.output_folder = OUTPUT_FOLDER
    
    def create_video(self, photo_paths, context, video_plan):
        """
        Create enhanced video from photos with transitions, effects, and better music
        """
        try:
            print(f"Creating enhanced video with {len(photo_paths)} photos")
            print(f"Photo paths: {photo_paths}")
            
            # Get video plan parameters
            sequence = video_plan.get('sequence', list(range(len(photo_paths))))
            duration_per_photo = video_plan.get('duration_per_photo', 4)  # Longer for effects
            music_style = video_plan.get('music_style', 'nostalgic')
            
            print(f"Video plan: sequence={sequence}, duration={duration_per_photo}, music={music_style}")
            
            # Create enhanced clips from photos
            clips = []
            for i, photo_idx in enumerate(sequence):
                if photo_idx < len(photo_paths):
                    photo_path = photo_paths[photo_idx]
                    print(f"Processing photo {i+1}/{len(sequence)}: {photo_path}")
                    
                    # Get effect for this photo
                    effect = self._get_photo_effect(i, len(sequence))
                    clip = self._create_enhanced_photo_clip(photo_path, duration_per_photo, effect)
                    
                    # Add transition
                    transition = self._get_transition(i, len(sequence))
                    clip = self._apply_transition(clip, transition, i, len(sequence))
                    
                    clips.append(clip)
                    print(f"Created enhanced clip {i+1} with duration {clip.duration}, effect: {effect}, transition: {transition}")
            
            if not clips:
                raise Exception("No valid clips were created")
            
            print(f"Concatenating {len(clips)} clips with transitions...")
            # Concatenate with transitions
            final_video = self._concatenate_with_transitions(clips)
            print(f"Final video duration: {final_video.duration}")
            
            # Add enhanced background music
            final_video = self._add_enhanced_background_music(final_video, music_style)
            
            # Generate output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"enhanced_memory_{timestamp}.mp4"
            output_path = os.path.join(self.output_folder, output_filename)
            
            print(f"Writing enhanced video to: {output_path}")
            # Write video file with high quality settings
            final_video.write_videofile(
                output_path,
                fps=30,  # Higher FPS for smooth effects
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                bitrate='3000k'  # High quality
            )
            
            print(f"Enhanced video created successfully: {output_path}")
            
            # Clean up
            final_video.close()
            for clip in clips:
                clip.close()
            
            return output_path
            
        except Exception as e:
            print(f"Error creating enhanced video: {str(e)}")
            import traceback
            traceback.print_exc()
            raise e
    
    def _get_photo_effect(self, index, total_photos):
        """Get visual effect for photo based on position"""
        if index == 0:
            return 'zoom_in'  # Start with zoom in
        elif index == total_photos - 1:
            return 'zoom_out'  # End with zoom out
        else:
            # Random effects for middle photos
            effects = ['pan_left', 'pan_right', 'zoom_in', 'zoom_out', 'static']
            return random.choice(effects)
    
    def _get_transition(self, index, total_photos):
        """Get transition for photo based on position"""
        if index == 0:
            return 'fade_in'  # First photo fades in
        elif index == total_photos - 1:
            return 'fade_out'  # Last photo fades out
        else:
            # Random transitions for middle photos
            transitions = ['crossfade', 'slide_left', 'slide_right', 'zoom', 'fade']
            return random.choice(transitions)
    
    def _create_enhanced_photo_clip(self, photo_path, duration, effect):
        """Create an enhanced video clip from a photo"""
        try:
            print(f"Creating enhanced clip from: {photo_path} with effect: {effect}")
            
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
            
            # Resize to video dimensions
            clip = self._resize_for_video(clip)
            print(f"Resized clip size: {clip.size}")
            
            # Apply visual effect
            clip = self._apply_visual_effect(clip, effect)
            
            return clip
            
        except Exception as e:
            print(f"Error creating enhanced clip from {photo_path}: {str(e)}")
            return self._create_fallback_clip(duration)
    
    def _create_fallback_clip(self, duration):
        """Create a fallback clip when image processing fails"""
        return ColorClip(size=(DEFAULT_VIDEO_WIDTH, DEFAULT_VIDEO_HEIGHT), color=(50, 50, 50), duration=duration)
    
    def _resize_for_video(self, clip):
        """Resize clip for video presentation"""
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
    
    def _apply_visual_effect(self, clip, effect):
        """Apply visual effects to clip"""
        try:
            if effect == 'zoom_in':
                return self._apply_zoom_in(clip)
            elif effect == 'zoom_out':
                return self._apply_zoom_out(clip)
            elif effect == 'pan_left':
                return self._apply_pan_left(clip)
            elif effect == 'pan_right':
                return self._apply_pan_right(clip)
            else:  # static
                return clip
        except Exception as e:
            print(f"Error applying visual effect {effect}: {str(e)}")
            return clip
    
    def _apply_zoom_in(self, clip):
        """Apply zoom in effect"""
        try:
            def zoom_effect(get_frame, t):
                frame = get_frame(t)
                if frame is None:
                    return frame
                
                h, w = frame.shape[:2]
                progress = t / clip.duration
                
                # Zoom from 1.0 to 1.2
                zoom = 1.0 + (0.2 * progress)
                
                new_h, new_w = int(h * zoom), int(w * zoom)
                if new_h > h or new_w > w:
                    start_h = (new_h - h) // 2
                    start_w = (new_w - w) // 2
                    end_h = start_h + h
                    end_w = start_w + w
                    
                    if start_h >= 0 and start_w >= 0 and end_h <= new_h and end_w <= new_w:
                        frame = frame[start_h:end_h, start_w:end_w]
                
                return frame
            
            return clip.time_transform(zoom_effect)
        except Exception as e:
            print(f"Error applying zoom in: {str(e)}")
            return clip
    
    def _apply_zoom_out(self, clip):
        """Apply zoom out effect"""
        try:
            def zoom_effect(get_frame, t):
                frame = get_frame(t)
                if frame is None:
                    return frame
                
                h, w = frame.shape[:2]
                progress = t / clip.duration
                
                # Zoom from 1.2 to 1.0
                zoom = 1.2 - (0.2 * progress)
                
                new_h, new_w = int(h * zoom), int(w * zoom)
                if new_h > h or new_w > w:
                    start_h = (new_h - h) // 2
                    start_w = (new_w - w) // 2
                    end_h = start_h + h
                    end_w = start_w + w
                    
                    if start_h >= 0 and start_w >= 0 and end_h <= new_h and end_w <= new_w:
                        frame = frame[start_h:end_h, start_w:end_w]
                
                return frame
            
            return clip.time_transform(zoom_effect)
        except Exception as e:
            print(f"Error applying zoom out: {str(e)}")
            return clip
    
    def _apply_pan_left(self, clip):
        """Apply pan left effect"""
        try:
            def pan_effect(get_frame, t):
                frame = get_frame(t)
                if frame is None:
                    return frame
                
                h, w = frame.shape[:2]
                progress = t / clip.duration
                
                # Pan from right to left
                pan_x = int(w * 0.15 * (1 - progress))
                
                if pan_x > 0:
                    frame = frame[:, pan_x:]
                
                return frame
            
            return clip.time_transform(pan_effect)
        except Exception as e:
            print(f"Error applying pan left: {str(e)}")
            return clip
    
    def _apply_pan_right(self, clip):
        """Apply pan right effect"""
        try:
            def pan_effect(get_frame, t):
                frame = get_frame(t)
                if frame is None:
                    return frame
                
                h, w = frame.shape[:2]
                progress = t / clip.duration
                
                # Pan from left to right
                pan_x = int(w * 0.15 * progress)
                
                if pan_x > 0:
                    frame = frame[:, :-pan_x] if pan_x < w else frame
                
                return frame
            
            return clip.time_transform(pan_effect)
        except Exception as e:
            print(f"Error applying pan right: {str(e)}")
            return clip
    
    def _apply_transition(self, clip, transition, index, total_clips):
        """Apply transitions to clip"""
        try:
            if transition == 'fade_in':
                # Simple fade in using opacity
                return clip.with_opacity(lambda t: min(1.0, t / 1.0))
            elif transition == 'fade_out':
                # Simple fade out using opacity
                return clip.with_opacity(lambda t: max(0.0, 1.0 - (t - (clip.duration - 1.0)) / 1.0))
            elif transition == 'crossfade':
                # Crossfade effect
                return clip.with_opacity(lambda t: min(1.0, t / 0.5) if t < 0.5 else max(0.0, 1.0 - (t - (clip.duration - 0.5)) / 0.5))
            elif transition == 'slide_left':
                # Slide left effect
                return clip.with_position(lambda t: (t * 100, 0))
            elif transition == 'slide_right':
                # Slide right effect
                return clip.with_position(lambda t: (-t * 100, 0))
            else:  # fade
                return clip.with_opacity(lambda t: min(1.0, t / 0.5) if t < 0.5 else max(0.0, 1.0 - (t - (clip.duration - 0.5)) / 0.5))
        except Exception as e:
            print(f"Error applying transition {transition}: {str(e)}")
            return clip
    
    def _concatenate_with_transitions(self, clips):
        """Concatenate clips with transitions"""
        try:
            if len(clips) == 1:
                return clips[0]
            
            # Create transition clips
            transition_clips = []
            
            for i, clip in enumerate(clips):
                if i == 0:
                    # First clip - fade in
                    transition_clips.append(clip.with_opacity(lambda t: min(1.0, t / 1.0)))
                elif i == len(clips) - 1:
                    # Last clip - fade out
                    transition_clips.append(clip.with_opacity(lambda t: max(0.0, 1.0 - (t - (clip.duration - 1.0)) / 1.0)))
                else:
                    # Middle clips - crossfade
                    transition_clips.append(clip.with_opacity(lambda t: min(1.0, t / 0.5) if t < 0.5 else max(0.0, 1.0 - (t - (clip.duration - 0.5)) / 0.5)))
            
            return concatenate_videoclips(transition_clips, method="compose")
        except Exception as e:
            print(f"Error concatenating with transitions: {str(e)}")
            return concatenate_videoclips(clips, method="compose")
    
    def _add_enhanced_background_music(self, video, music_style):
        """Add enhanced background music to video"""
        try:
            print(f"Adding {music_style} enhanced background music...")
            
            # Generate enhanced music based on style
            music = self._create_enhanced_music(music_style, video.duration)
            
            # Set volume using the correct method
            music = music.with_volume_scaled(0.4)  # 40% volume
            
            return video.with_audio(music)
        except Exception as e:
            print(f"Error adding enhanced background music: {str(e)}")
            return video
    
    def _create_enhanced_music(self, style, duration):
        """Create enhanced music based on style"""
        def make_frame(t):
            if style == 'nostalgic':
                # Enhanced nostalgic melody with multiple frequencies
                freq1 = 220  # A3
                freq2 = 277  # C#4
                freq3 = 330  # E4
                freq4 = 392  # G4
                
                # Create chord progression
                wave1 = np.sin(2 * np.pi * freq1 * t) * 0.3
                wave2 = np.sin(2 * np.pi * freq2 * t) * 0.25
                wave3 = np.sin(2 * np.pi * freq3 * t) * 0.2
                wave4 = np.sin(2 * np.pi * freq4 * t) * 0.15
                
                # Add some reverb-like effect
                reverb = np.sin(2 * np.pi * 0.5 * t) * 0.1
                
                return wave1 + wave2 + wave3 + wave4 + reverb
                
            elif style == 'upbeat':
                # Enhanced upbeat melody
                freq1 = 440  # A4
                freq2 = 554  # C#5
                freq3 = 659  # E5
                freq4 = 784  # G5
                
                # Fast tempo with rhythm
                wave1 = np.sin(2 * np.pi * freq1 * t * 1.5) * 0.3
                wave2 = np.sin(2 * np.pi * freq2 * t * 1.5) * 0.25
                wave3 = np.sin(2 * np.pi * freq3 * t * 1.5) * 0.2
                wave4 = np.sin(2 * np.pi * freq4 * t * 1.5) * 0.15
                
                # Add rhythm
                rhythm = np.sin(2 * np.pi * 3 * t) * 0.1
                
                return wave1 + wave2 + wave3 + wave4 + rhythm
                
            elif style == 'romantic':
                # Enhanced romantic melody
                freq1 = 392  # G4
                freq2 = 494  # B4
                freq3 = 587  # D5
                freq4 = 659  # E5
                
                # Soft attack with envelope
                envelope = np.exp(-t * 0.2) if t < 2 else 0.6
                
                wave1 = np.sin(2 * np.pi * freq1 * t) * 0.3 * envelope
                wave2 = np.sin(2 * np.pi * freq2 * t) * 0.25 * envelope
                wave3 = np.sin(2 * np.pi * freq3 * t) * 0.2 * envelope
                wave4 = np.sin(2 * np.pi * freq4 * t) * 0.15 * envelope
                
                return wave1 + wave2 + wave3 + wave4
                
            elif style == 'energetic':
                # Enhanced energetic melody
                freq1 = 523  # C5
                freq2 = 659  # E5
                freq3 = 784  # G5
                freq4 = 880  # A5
                
                # Very fast tempo
                wave1 = np.sin(2 * np.pi * freq1 * t * 2) * 0.3
                wave2 = np.sin(2 * np.pi * freq2 * t * 2) * 0.25
                wave3 = np.sin(2 * np.pi * freq3 * t * 2) * 0.2
                wave4 = np.sin(2 * np.pi * freq4 * t * 2) * 0.15
                
                # Add percussion
                percussion = np.sin(2 * np.pi * 6 * t) * 0.1
                
                return wave1 + wave2 + wave3 + wave4 + percussion
                
            else:  # calm
                # Enhanced calm melody
                freq1 = 220  # A3
                freq2 = 277  # C#4
                freq3 = 330  # E4
                freq4 = 392  # G4
                
                # Very slow tempo
                wave1 = np.sin(2 * np.pi * freq1 * t * 0.4) * 0.3
                wave2 = np.sin(2 * np.pi * freq2 * t * 0.4) * 0.25
                wave3 = np.sin(2 * np.pi * freq3 * t * 0.4) * 0.2
                wave4 = np.sin(2 * np.pi * freq4 * t * 0.4) * 0.15
                
                return wave1 + wave2 + wave3 + wave4
        
        return AudioClip(make_frame, duration=duration)

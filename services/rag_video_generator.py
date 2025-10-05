import os
import moviepy
from moviepy import VideoFileClip, ImageClip, ColorClip, concatenate_videoclips, AudioClip
from PIL import Image
import numpy as np
from datetime import datetime
from config import *

class RAGVideoGenerator:
    def __init__(self):
        self.output_folder = OUTPUT_FOLDER
    
    def create_video(self, photo_paths, context, video_plan):
        """
        Create video using RAG-based planning
        """
        try:
            print(f"Creating RAG-based video with {len(photo_paths)} photos")
            print(f"Photo paths: {photo_paths}")
            print(f"Video plan: {video_plan}")
            
            # Get video plan parameters
            sequence = video_plan.get('sequence', list(range(len(photo_paths))))
            effects = video_plan.get('effects', ['static'] * len(photo_paths))
            transitions = video_plan.get('transitions', ['fade'] * len(photo_paths))
            duration_per_photo = video_plan.get('duration_per_photo', 3)
            music_style = video_plan.get('music_style', 'nostalgic')
            
            print(f"Sequence: {sequence}")
            print(f"Effects: {effects}")
            print(f"Transitions: {transitions}")
            print(f"Duration per photo: {duration_per_photo}")
            print(f"Music style: {music_style}")
            
            # Create clips from photos
            clips = []
            for i, photo_idx in enumerate(sequence):
                if photo_idx < len(photo_paths):
                    photo_path = photo_paths[photo_idx]
                    effect = effects[i] if i < len(effects) else 'static'
                    transition = transitions[i] if i < len(transitions) else 'fade'
                    
                    print(f"Processing photo {i+1}/{len(sequence)}: {photo_path}")
                    print(f"Effect: {effect}, Transition: {transition}")
                    
                    # Create clip with effect
                    clip = self._create_photo_clip_with_effect(photo_path, duration_per_photo, effect)
                    clips.append(clip)
                    print(f"Created clip {i+1} with duration {clip.duration}")
            
            if not clips:
                raise Exception("No valid clips were created")
            
            print(f"Concatenating {len(clips)} clips...")
            # Simple concatenation (transitions will be handled by effects)
            final_video = concatenate_videoclips(clips, method="compose")
            print(f"Final video duration: {final_video.duration}")
            
            # Add background music
            final_video = self._add_background_music(final_video, music_style)
            
            # Generate output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"rag_memory_{timestamp}.mp4"
            output_path = os.path.join(self.output_folder, output_filename)
            
            print(f"Writing RAG video to: {output_path}")
            # Write video file
            final_video.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio_codec='aac'
            )
            
            print(f"RAG video created successfully: {output_path}")
            
            # Clean up
            final_video.close()
            for clip in clips:
                clip.close()
            
            return output_path
            
        except Exception as e:
            print(f"Error creating RAG video: {str(e)}")
            import traceback
            traceback.print_exc()
            raise e
    
    def _create_photo_clip_with_effect(self, photo_path, duration, effect):
        """Create a photo clip with the specified effect"""
        try:
            print(f"Creating clip from: {photo_path} with effect: {effect}")
            
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
            
            # Resize to fit video dimensions
            clip = self._resize_for_video(clip)
            print(f"Resized clip size: {clip.size}")
            
            # Apply effect
            clip = self._apply_effect(clip, effect)
            
            return clip
            
        except Exception as e:
            print(f"Error creating clip from {photo_path}: {str(e)}")
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
    
    def _apply_effect(self, clip, effect):
        """Apply the specified effect to the clip"""
        try:
            if effect == 'ken_burns_zoom_in':
                return self._apply_ken_burns_zoom_in(clip)
            elif effect == 'ken_burns_zoom_out':
                return self._apply_ken_burns_zoom_out(clip)
            elif effect == 'pan_left':
                return self._apply_pan_left(clip)
            elif effect == 'pan_right':
                return self._apply_pan_right(clip)
            elif effect == 'zoom_in_center':
                return self._apply_zoom_in_center(clip)
            elif effect == 'zoom_out_center':
                return self._apply_zoom_out_center(clip)
            else:  # static
                return clip
        except Exception as e:
            print(f"Error applying effect {effect}: {str(e)}")
            return clip
    
    def _apply_ken_burns_zoom_in(self, clip):
        """Apply Ken Burns zoom in effect"""
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
            print(f"Error applying Ken Burns zoom in: {str(e)}")
            return clip
    
    def _apply_ken_burns_zoom_out(self, clip):
        """Apply Ken Burns zoom out effect"""
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
            print(f"Error applying Ken Burns zoom out: {str(e)}")
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
    
    def _apply_zoom_in_center(self, clip):
        """Apply zoom in center effect"""
        try:
            def zoom_effect(get_frame, t):
                frame = get_frame(t)
                if frame is None:
                    return frame
                
                h, w = frame.shape[:2]
                progress = t / clip.duration
                
                # Zoom in from center
                zoom = 1.0 + (0.3 * progress)
                
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
            print(f"Error applying zoom in center: {str(e)}")
            return clip
    
    def _apply_zoom_out_center(self, clip):
        """Apply zoom out center effect"""
        try:
            def zoom_effect(get_frame, t):
                frame = get_frame(t)
                if frame is None:
                    return frame
                
                h, w = frame.shape[:2]
                progress = t / clip.duration
                
                # Zoom out from center
                zoom = 1.3 - (0.3 * progress)
                
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
            print(f"Error applying zoom out center: {str(e)}")
            return clip
    
    def _add_background_music(self, video, music_style):
        """Add background music to video"""
        try:
            print(f"Adding {music_style} background music...")
            
            # Generate music based on style
            music = self._create_music(music_style, video.duration)
            
            # Set volume
            music = music.with_volume_scaled(0.3)  # 30% volume
            
            return video.with_audio(music)
        except Exception as e:
            print(f"Error adding background music: {str(e)}")
            return video
    
    def _create_music(self, style, duration):
        """Create enhanced music based on RAG database style"""
        def make_frame(t):
            # Handle both single values and arrays
            if hasattr(t, '__len__') and len(t) > 1:
                t = t[0] if len(t) > 0 else 0
            
            if style == 'nostalgic':
                # Enhanced nostalgic melody with warm tones
                freq1 = 220  # A3 - warm base
                freq2 = 277  # C#4 - emotional
                freq3 = 330  # E4 - nostalgic
                freq4 = 392  # G4 - warm harmony
                
                # Create chord progression with envelope
                envelope = np.exp(-t * 0.1) if t < 3 else 0.7
                
                wave1 = np.sin(2 * np.pi * freq1 * t) * 0.3 * envelope
                wave2 = np.sin(2 * np.pi * freq2 * t) * 0.25 * envelope
                wave3 = np.sin(2 * np.pi * freq3 * t) * 0.2 * envelope
                wave4 = np.sin(2 * np.pi * freq4 * t) * 0.15 * envelope
                
                # Add some reverb-like effect
                reverb = np.sin(2 * np.pi * 0.5 * t) * 0.1 * envelope
                
                return wave1 + wave2 + wave3 + wave4 + reverb
                
            elif style == 'upbeat':
                # Enhanced upbeat melody with bright tones
                freq1 = 440  # A4 - bright
                freq2 = 554  # C#5 - energetic
                freq3 = 659  # E5 - celebratory
                freq4 = 784  # G5 - exciting
                
                # Fast tempo with rhythm
                tempo = 1.5
                wave1 = np.sin(2 * np.pi * freq1 * t * tempo) * 0.3
                wave2 = np.sin(2 * np.pi * freq2 * t * tempo) * 0.25
                wave3 = np.sin(2 * np.pi * freq3 * t * tempo) * 0.2
                wave4 = np.sin(2 * np.pi * freq4 * t * tempo) * 0.15
                
                # Add rhythm
                rhythm = np.sin(2 * np.pi * 4 * t) * 0.1
                
                return wave1 + wave2 + wave3 + wave4 + rhythm
                
            elif style == 'romantic':
                # Enhanced romantic melody with soft tones
                freq1 = 392  # G4 - romantic
                freq2 = 494  # B4 - intimate
                freq3 = 587  # D5 - loving
                freq4 = 659  # E5 - tender
                
                # Soft attack with envelope
                envelope = np.exp(-t * 0.2) if t < 2 else 0.6
                
                wave1 = np.sin(2 * np.pi * freq1 * t) * 0.3 * envelope
                wave2 = np.sin(2 * np.pi * freq2 * t) * 0.25 * envelope
                wave3 = np.sin(2 * np.pi * freq3 * t) * 0.2 * envelope
                wave4 = np.sin(2 * np.pi * freq4 * t) * 0.15 * envelope
                
                return wave1 + wave2 + wave3 + wave4
                
            elif style == 'energetic':
                # Enhanced energetic melody with dynamic tones
                freq1 = 523  # C5 - energetic
                freq2 = 659  # E5 - exciting
                freq3 = 784  # G5 - dynamic
                freq4 = 880  # A5 - powerful
                
                # Very fast tempo
                tempo = 2.0
                wave1 = np.sin(2 * np.pi * freq1 * t * tempo) * 0.3
                wave2 = np.sin(2 * np.pi * freq2 * t * tempo) * 0.25
                wave3 = np.sin(2 * np.pi * freq3 * t * tempo) * 0.2
                wave4 = np.sin(2 * np.pi * freq4 * t * tempo) * 0.15
                
                # Add percussion
                percussion = np.sin(2 * np.pi * 6 * t) * 0.1
                
                return wave1 + wave2 + wave3 + wave4 + percussion
                
            elif style == 'dramatic':
                # Enhanced dramatic melody with intense tones
                freq1 = 220  # A3 - dramatic base
                freq2 = 277  # C#4 - intense
                freq3 = 330  # E4 - powerful
                freq4 = 392  # G4 - dramatic
                
                # Variable intensity
                intensity = 0.5 + 0.3 * np.sin(t * 0.5)
                
                wave1 = np.sin(2 * np.pi * freq1 * t) * 0.4 * intensity
                wave2 = np.sin(2 * np.pi * freq2 * t) * 0.3 * intensity
                wave3 = np.sin(2 * np.pi * freq3 * t) * 0.2 * intensity
                wave4 = np.sin(2 * np.pi * freq4 * t) * 0.15 * intensity
                
                return wave1 + wave2 + wave3 + wave4
                
            else:  # calm
                # Enhanced calm melody with peaceful tones
                freq1 = 220  # A3 - peaceful
                freq2 = 277  # C#4 - serene
                freq3 = 330  # E4 - calm
                freq4 = 392  # G4 - relaxing
                
                # Very slow tempo
                tempo = 0.5
                wave1 = np.sin(2 * np.pi * freq1 * t * tempo) * 0.2
                wave2 = np.sin(2 * np.pi * freq2 * t * tempo) * 0.15
                wave3 = np.sin(2 * np.pi * freq3 * t * tempo) * 0.1
                wave4 = np.sin(2 * np.pi * freq4 * t * tempo) * 0.05
                
                return wave1 + wave2 + wave3 + wave4
        
        return AudioClip(make_frame, duration=duration)

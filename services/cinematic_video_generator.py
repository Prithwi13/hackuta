import os
import moviepy
from moviepy import VideoFileClip, ImageClip, ColorClip, concatenate_videoclips, AudioClip, CompositeVideoClip
from PIL import Image
import random
import numpy as np
from datetime import datetime
from config import *

class CinematicVideoGenerator:
    def __init__(self):
        self.output_folder = OUTPUT_FOLDER
        self.music_styles = {
            'nostalgic': self._create_nostalgic_music,
            'upbeat': self._create_upbeat_music,
            'romantic': self._create_romantic_music,
            'energetic': self._create_energetic_music,
            'calm': self._create_calm_music
        }
    
    def create_video(self, photo_paths, context, video_plan):
        """
        Create cinematic video from photos with professional transitions and music
        """
        try:
            print(f"Creating cinematic video with {len(photo_paths)} photos")
            print(f"Photo paths: {photo_paths}")
            
            # Get video plan parameters
            sequence = video_plan.get('sequence', list(range(len(photo_paths))))
            duration_per_photo = video_plan.get('duration_per_photo', 4)  # Longer for cinematic feel
            music_style = video_plan.get('music_style', 'nostalgic')
            
            print(f"Video plan: sequence={sequence}, duration={duration_per_photo}, music={music_style}")
            
            # Create cinematic clips from photos
            clips = []
            for i, photo_idx in enumerate(sequence):
                if photo_idx < len(photo_paths):
                    photo_path = photo_paths[photo_idx]
                    print(f"Processing photo {i+1}/{len(sequence)}: {photo_path}")
                    
                    # Get cinematic effect for this photo
                    effect = self._get_cinematic_effect(i, len(sequence))
                    clip = self._create_cinematic_photo_clip(photo_path, duration_per_photo, effect)
                    
                    # Add cinematic transition
                    transition = self._get_cinematic_transition(i, len(sequence))
                    clip = self._apply_cinematic_transition(clip, transition, i, len(sequence))
                    
                    clips.append(clip)
                    print(f"Created cinematic clip {i+1} with duration {clip.duration}, effect: {effect}, transition: {transition}")
            
            if not clips:
                raise Exception("No valid clips were created")
            
            print(f"Concatenating {len(clips)} clips...")
            # Concatenate clips with crossfade transitions
            final_video = self._concatenate_with_crossfades(clips)
            print(f"Final video duration: {final_video.duration}")
            
            # Add cinematic background music
            final_video = self._add_cinematic_background_music(final_video, music_style)
            
            # Generate output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"cinematic_memory_{timestamp}.mp4"
            output_path = os.path.join(self.output_folder, output_filename)
            
            print(f"Writing cinematic video to: {output_path}")
            # Write video file with high quality settings
            final_video.write_videofile(
                output_path,
                fps=30,  # Higher FPS for smooth cinematic feel
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                bitrate='5000k'  # High quality
            )
            
            print(f"Cinematic video created successfully: {output_path}")
            
            # Clean up
            final_video.close()
            for clip in clips:
                clip.close()
            
            return output_path
            
        except Exception as e:
            print(f"Error creating cinematic video: {str(e)}")
            import traceback
            traceback.print_exc()
            raise e
    
    def _get_cinematic_effect(self, index, total_photos):
        """Get cinematic effect for photo based on position"""
        if index == 0:
            return 'ken_burns_zoom_in'  # Start with zoom in
        elif index == total_photos - 1:
            return 'ken_burns_zoom_out'  # End with zoom out
        else:
            # Random cinematic effects for middle photos
            effects = ['ken_burns_pan_left', 'ken_burns_pan_right', 'ken_burns_zoom_in', 'ken_burns_zoom_out', 'static']
            return random.choice(effects)
    
    def _get_cinematic_transition(self, index, total_photos):
        """Get cinematic transition for photo based on position"""
        if index == 0:
            return 'fade_in'  # First photo fades in
        elif index == total_photos - 1:
            return 'fade_out'  # Last photo fades out
        else:
            # Cinematic transitions for middle photos
            transitions = ['crossfade', 'slide_left', 'slide_right', 'zoom_transition', 'fade']
            return random.choice(transitions)
    
    def _create_cinematic_photo_clip(self, photo_path, duration, effect):
        """Create a cinematic video clip from a photo"""
        try:
            print(f"Creating cinematic clip from: {photo_path} with effect: {effect}")
            
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
            
            # Resize to cinematic dimensions
            clip = self._resize_for_cinematic(clip)
            print(f"Resized clip size: {clip.size}")
            
            # Apply cinematic effect
            clip = self._apply_cinematic_effect(clip, effect)
            
            return clip
            
        except Exception as e:
            print(f"Error creating cinematic clip from {photo_path}: {str(e)}")
            return self._create_fallback_clip(duration)
    
    def _create_fallback_clip(self, duration):
        """Create a fallback clip when image processing fails"""
        return ColorClip(size=(DEFAULT_VIDEO_WIDTH, DEFAULT_VIDEO_HEIGHT), color=(50, 50, 50), duration=duration)
    
    def _resize_for_cinematic(self, clip):
        """Resize clip for cinematic presentation"""
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
    
    def _apply_cinematic_effect(self, clip, effect):
        """Apply cinematic visual effects to clip"""
        try:
            if effect == 'ken_burns_zoom_in':
                return self._apply_ken_burns_zoom_in(clip)
            elif effect == 'ken_burns_zoom_out':
                return self._apply_ken_burns_zoom_out(clip)
            elif effect == 'ken_burns_pan_left':
                return self._apply_ken_burns_pan_left(clip)
            elif effect == 'ken_burns_pan_right':
                return self._apply_ken_burns_pan_right(clip)
            else:  # static
                return clip
        except Exception as e:
            print(f"Error applying cinematic effect {effect}: {str(e)}")
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
    
    def _apply_ken_burns_pan_left(self, clip):
        """Apply Ken Burns pan left effect"""
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
            print(f"Error applying Ken Burns pan left: {str(e)}")
            return clip
    
    def _apply_ken_burns_pan_right(self, clip):
        """Apply Ken Burns pan right effect"""
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
            print(f"Error applying Ken Burns pan right: {str(e)}")
            return clip
    
    def _apply_cinematic_transition(self, clip, transition, index, total_clips):
        """Apply cinematic transitions between clips"""
        try:
            if transition == 'fade_in':
                return clip.fadein(1.0)  # Slow fade in
            elif transition == 'fade_out':
                return clip.fadeout(1.0)  # Slow fade out
            elif transition == 'crossfade':
                return clip.fadein(0.5).fadeout(0.5)
            elif transition == 'slide_left':
                return clip.with_position(lambda t: (t * 100, 0)).fadein(0.3).fadeout(0.3)
            elif transition == 'slide_right':
                return clip.with_position(lambda t: (-t * 100, 0)).fadein(0.3).fadeout(0.3)
            elif transition == 'zoom_transition':
                return clip.fadein(0.5).fadeout(0.5)
            else:  # fade
                return clip.fadein(0.5).fadeout(0.5)
        except Exception as e:
            print(f"Error applying cinematic transition {transition}: {str(e)}")
            return clip
    
    def _concatenate_with_crossfades(self, clips):
        """Concatenate clips with crossfade transitions"""
        try:
            if len(clips) == 1:
                return clips[0]
            
            # Create crossfade transitions between clips
            final_clips = [clips[0]]
            
            for i in range(1, len(clips)):
                # Add crossfade between clips
                crossfade_duration = 0.5
                clip1 = clips[i-1].fadeout(crossfade_duration)
                clip2 = clips[i].fadein(crossfade_duration)
                
                # Composite the crossfade
                crossfade = CompositeVideoClip([clip1, clip2])
                final_clips.append(crossfade)
            
            return concatenate_videoclips(final_clips, method="compose")
        except Exception as e:
            print(f"Error concatenating with crossfades: {str(e)}")
            return concatenate_videoclips(clips, method="compose")
    
    def _add_cinematic_background_music(self, video, music_style):
        """Add cinematic background music to video"""
        try:
            print(f"Adding {music_style} cinematic background music...")
            
            # Generate cinematic music based on style
            music = self.music_styles[music_style](video.duration)
            
            # Set volume for cinematic feel
            music = music.with_volume_scaled(0.4)  # Slightly louder for cinematic feel
            
            # Add cinematic fade in/out to music
            music = music.fadein(2.0).fadeout(2.0)  # Longer fades for cinematic feel
            
            return video.with_audio(music)
        except Exception as e:
            print(f"Error adding cinematic background music: {str(e)}")
            return video
    
    def _create_nostalgic_music(self, duration):
        """Create nostalgic, emotional music"""
        def make_frame(t):
            # Create a beautiful, emotional melody
            freq1 = 220  # A3 note
            freq2 = 277  # C#4 note
            freq3 = 330  # E4 note
            freq4 = 392  # G4 note
            
            # Create chord progression
            wave1 = np.sin(2 * np.pi * freq1 * t) * 0.3
            wave2 = np.sin(2 * np.pi * freq2 * t) * 0.25
            wave3 = np.sin(2 * np.pi * freq3 * t) * 0.2
            wave4 = np.sin(2 * np.pi * freq4 * t) * 0.15
            
            # Add some reverb-like effect
            reverb = np.sin(2 * np.pi * 0.5 * t) * 0.1
            
            return wave1 + wave2 + wave3 + wave4 + reverb
        
        return AudioClip(make_frame, duration=duration)
    
    def _create_upbeat_music(self, duration):
        """Create upbeat, happy music"""
        def make_frame(t):
            # Create an energetic melody
            freq1 = 440  # A4 note
            freq2 = 554  # C#5 note
            freq3 = 659  # E5 note
            freq4 = 784  # G5 note
            
            # Fast tempo
            wave1 = np.sin(2 * np.pi * freq1 * t * 1.5) * 0.3
            wave2 = np.sin(2 * np.pi * freq2 * t * 1.5) * 0.25
            wave3 = np.sin(2 * np.pi * freq3 * t * 1.5) * 0.2
            wave4 = np.sin(2 * np.pi * freq4 * t * 1.5) * 0.15
            
            # Add rhythm
            rhythm = np.sin(2 * np.pi * 3 * t) * 0.1
            
            return wave1 + wave2 + wave3 + wave4 + rhythm
        
        return AudioClip(make_frame, duration=duration)
    
    def _create_romantic_music(self, duration):
        """Create romantic, soft music"""
        def make_frame(t):
            # Create a soft, romantic melody
            freq1 = 392  # G4 note
            freq2 = 494  # B4 note
            freq3 = 587  # D5 note
            freq4 = 659  # E5 note
            
            # Soft attack
            envelope = np.exp(-t * 0.2) if t < 2 else 0.6
            
            wave1 = np.sin(2 * np.pi * freq1 * t) * 0.3 * envelope
            wave2 = np.sin(2 * np.pi * freq2 * t) * 0.25 * envelope
            wave3 = np.sin(2 * np.pi * freq3 * t) * 0.2 * envelope
            wave4 = np.sin(2 * np.pi * freq4 * t) * 0.15 * envelope
            
            return wave1 + wave2 + wave3 + wave4
        
        return AudioClip(make_frame, duration=duration)
    
    def _create_energetic_music(self, duration):
        """Create energetic, fast-paced music"""
        def make_frame(t):
            # Create high-energy music
            freq1 = 523  # C5 note
            freq2 = 659  # E5 note
            freq3 = 784  # G5 note
            freq4 = 880  # A5 note
            
            # Very fast tempo
            wave1 = np.sin(2 * np.pi * freq1 * t * 2) * 0.3
            wave2 = np.sin(2 * np.pi * freq2 * t * 2) * 0.25
            wave3 = np.sin(2 * np.pi * freq3 * t * 2) * 0.2
            wave4 = np.sin(2 * np.pi * freq4 * t * 2) * 0.15
            
            # Add percussion
            percussion = np.sin(2 * np.pi * 6 * t) * 0.1
            
            return wave1 + wave2 + wave3 + wave4 + percussion
        
        return AudioClip(make_frame, duration=duration)
    
    def _create_calm_music(self, duration):
        """Create calm, peaceful music"""
        def make_frame(t):
            # Create peaceful music
            freq1 = 220  # A3 note
            freq2 = 277  # C#4 note
            freq3 = 330  # E4 note
            freq4 = 392  # G4 note
            
            # Very slow tempo
            wave1 = np.sin(2 * np.pi * freq1 * t * 0.4) * 0.3
            wave2 = np.sin(2 * np.pi * freq2 * t * 0.4) * 0.25
            wave3 = np.sin(2 * np.pi * freq3 * t * 0.4) * 0.2
            wave4 = np.sin(2 * np.pi * freq4 * t * 0.4) * 0.15
            
            return wave1 + wave2 + wave3 + wave4
        
        return AudioClip(make_frame, duration=duration)

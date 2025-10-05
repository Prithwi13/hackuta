import os
import moviepy
from moviepy import VideoFileClip, ImageClip, ColorClip, concatenate_videoclips, AudioClip, CompositeVideoClip
from PIL import Image
import random
import numpy as np
from datetime import datetime
from config import *
from services.music_service import MusicService

class VideoGenerator:
    def __init__(self):
        self.output_folder = OUTPUT_FOLDER
        self.music_service = MusicService()
        self.transition_types = ['fade', 'slide_left', 'slide_right', 'zoom_in', 'zoom_out', 'crossfade']
        self.effect_types = ['ken_burns', 'pan_left', 'pan_right', 'zoom_in', 'zoom_out', 'static']
    
    def create_video(self, photo_paths, context, video_plan):
        """
        Create video from photos with transitions and music
        """
        try:
            print(f"Creating video with {len(photo_paths)} photos")
            print(f"Photo paths: {photo_paths}")
            
            # Get video plan parameters
            sequence = video_plan.get('sequence', list(range(len(photo_paths))))
            transitions = video_plan.get('transitions', self._generate_transitions(len(photo_paths)))
            duration_per_photo = video_plan.get('duration_per_photo', 3)
            video_style = video_plan.get('video_style', 'modern')
            music_style = video_plan.get('music_style', 'nostalgic')
            
            print(f"Video plan: sequence={sequence}, transitions={transitions}, duration={duration_per_photo}")
            
            # Create clips from photos with enhanced effects
            clips = []
            for i, photo_idx in enumerate(sequence):
                if photo_idx < len(photo_paths):
                    photo_path = photo_paths[photo_idx]
                    print(f"Processing photo {i+1}/{len(sequence)}: {photo_path}")
                    
                    # Get transition and effect for this photo
                    transition = transitions[i] if i < len(transitions) else 'fade'
                    effect = self._get_photo_effect(i, len(sequence))
                    
                    clip = self._create_enhanced_photo_clip(photo_path, duration_per_photo, effect)
                    
                    # Apply transition
                    clip = self._apply_enhanced_transition(clip, transition, i, len(sequence))
                    
                    clips.append(clip)
                    print(f"Created clip {i+1} with duration {clip.duration}, effect: {effect}, transition: {transition}")
            
            if not clips:
                raise Exception("No valid clips were created")
            
            print(f"Concatenating {len(clips)} clips...")
            # Concatenate clips
            final_video = concatenate_videoclips(clips, method="compose")
            print(f"Final video duration: {final_video.duration}")
            
            # Add enhanced background music
            final_video = self._add_enhanced_background_music(final_video, music_style)
            
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
    
    def _create_photo_clip(self, photo_path, duration):
        """Create a video clip from a photo"""
        try:
            print(f"Creating clip from: {photo_path}")
            
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
            
            # Resize to standard dimensions while maintaining aspect ratio
            clip = self._resize_clip(clip)
            print(f"Resized clip size: {clip.size}")
            
            # Apply Ken Burns effect
            clip = self._apply_ken_burns(clip)
            
            return clip
            
        except Exception as e:
            print(f"Error creating clip from {photo_path}: {str(e)}")
            return self._create_fallback_clip(duration)
    
    def _create_fallback_clip(self, duration):
        """Create a fallback clip when image processing fails"""
        return ColorClip(size=(DEFAULT_VIDEO_WIDTH, DEFAULT_VIDEO_HEIGHT), color=(100, 100, 100), duration=duration)
    
    def _resize_clip(self, clip):
        """Resize clip to standard dimensions while maintaining aspect ratio"""
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
            
            # Center the clip on the canvas
            x_center = (DEFAULT_VIDEO_WIDTH - new_w) // 2
            y_center = (DEFAULT_VIDEO_HEIGHT - new_h) // 2
            
            # Create a background clip and composite
            background = ColorClip(size=(DEFAULT_VIDEO_WIDTH, DEFAULT_VIDEO_HEIGHT), color=(0, 0, 0), duration=clip.duration)
            # Use correct positioning method
            clip = clip.with_position((x_center, y_center))
            
            return clip
            
        except Exception as e:
            print(f"Error resizing clip: {str(e)}")
            return clip
    
    def _apply_ken_burns(self, clip):
        """Apply Ken Burns zoom effect"""
        try:
            # Simple zoom effect - start slightly zoomed in, end at normal size
            start_scale = 1.1
            end_scale = 1.0
            
            def zoom_effect(get_frame, t):
                # Calculate scale factor based on time
                progress = t / clip.duration
                scale = start_scale + (end_scale - start_scale) * progress
                
                # Get the frame and apply scaling
                frame = get_frame(t)
                if frame is not None:
                    # Simple zoom by cropping and resizing
                    h, w = frame.shape[:2]
                    new_h, new_w = int(h * scale), int(w * scale)
                    
                    if new_h > h or new_w > w:
                        # Crop from center
                        start_h = (new_h - h) // 2
                        start_w = (new_w - w) // 2
                        frame = frame[start_h:start_h+h, start_w:start_w+w]
                
                return frame
            
            return clip.time_transform(zoom_effect)
        except Exception as e:
            print(f"Error applying Ken Burns effect: {str(e)}")
            return clip
    
    def _apply_transition(self, clip, transition_type):
        """Apply transition effect to clip"""
        try:
            if transition_type == 'fade':
                return clip.fadein(0.5).fadeout(0.5)
            elif transition_type == 'slide':
                # Simple slide effect
                return clip.with_position(lambda t: (t * 50, 0))
            else:
                # Default: just add fade in/out
                return clip.fadein(0.3).fadeout(0.3)
        except Exception as e:
            print(f"Error applying transition: {str(e)}")
            return clip
    
    def _generate_transitions(self, num_photos):
        """Generate a variety of transitions for the video"""
        transitions = []
        for i in range(num_photos):
            if i == 0:
                transitions.append('fade')  # First photo just fades in
            elif i == num_photos - 1:
                transitions.append('fade')  # Last photo just fades out
            else:
                # Random transition for middle photos
                transitions.append(random.choice(self.transition_types[1:]))
        return transitions
    
    def _get_photo_effect(self, index, total_photos):
        """Get visual effect for a photo based on its position"""
        if index == 0:
            return 'ken_burns'  # First photo gets Ken Burns
        elif index == total_photos - 1:
            return 'zoom_out'  # Last photo zooms out
        else:
            # Random effect for middle photos
            return random.choice(self.effect_types)
    
    def _create_enhanced_photo_clip(self, photo_path, duration, effect):
        """Create a photo clip with enhanced visual effects"""
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
            
            # Resize to standard dimensions
            clip = self._resize_clip(clip)
            print(f"Resized clip size: {clip.size}")
            
            # Apply visual effect
            clip = self._apply_visual_effect(clip, effect)
            
            return clip
            
        except Exception as e:
            print(f"Error creating enhanced clip from {photo_path}: {str(e)}")
            return self._create_fallback_clip(duration)
    
    def _apply_visual_effect(self, clip, effect):
        """Apply visual effects to clip"""
        try:
            if effect == 'ken_burns':
                return self._apply_ken_burns_enhanced(clip)
            elif effect == 'pan_left':
                return self._apply_pan_left(clip)
            elif effect == 'pan_right':
                return self._apply_pan_right(clip)
            elif effect == 'zoom_in':
                return self._apply_zoom_in(clip)
            elif effect == 'zoom_out':
                return self._apply_zoom_out(clip)
            else:  # static
                return clip
        except Exception as e:
            print(f"Error applying visual effect {effect}: {str(e)}")
            return clip
    
    def _apply_ken_burns_enhanced(self, clip):
        """Enhanced Ken Burns effect with zoom and pan"""
        try:
            def ken_burns_effect(get_frame, t):
                frame = get_frame(t)
                if frame is None:
                    return frame
                
                h, w = frame.shape[:2]
                progress = t / clip.duration
                
                # Zoom from 1.1 to 1.0
                zoom = 1.1 - (0.1 * progress)
                
                # Pan from left to right
                pan_x = int((w * 0.1) * progress)
                
                # Apply zoom and pan
                new_h, new_w = int(h * zoom), int(w * zoom)
                if new_h > h or new_w > w:
                    # Crop and resize
                    start_h = max(0, (new_h - h) // 2)
                    start_w = max(0, (new_w - w) // 2 + pan_x)
                    end_h = min(new_h, start_h + h)
                    end_w = min(new_w, start_w + w)
                    
                    if start_h < end_h and start_w < end_w:
                        frame = frame[start_h:end_h, start_w:end_w]
                
                return frame
            
            return clip.time_transform(ken_burns_effect)
        except Exception as e:
            print(f"Error applying enhanced Ken Burns: {str(e)}")
            return clip
    
    def _apply_pan_left(self, clip):
        """Pan effect moving from right to left"""
        try:
            def pan_effect(get_frame, t):
                frame = get_frame(t)
                if frame is None:
                    return frame
                
                h, w = frame.shape[:2]
                progress = t / clip.duration
                
                # Pan from right to left
                pan_x = int(w * 0.2 * (1 - progress))
                
                # Crop and shift
                if pan_x > 0:
                    frame = frame[:, pan_x:]
                
                return frame
            
            return clip.time_transform(pan_effect)
        except Exception as e:
            print(f"Error applying pan left: {str(e)}")
            return clip
    
    def _apply_pan_right(self, clip):
        """Pan effect moving from left to right"""
        try:
            def pan_effect(get_frame, t):
                frame = get_frame(t)
                if frame is None:
                    return frame
                
                h, w = frame.shape[:2]
                progress = t / clip.duration
                
                # Pan from left to right
                pan_x = int(w * 0.2 * progress)
                
                # Crop and shift
                if pan_x > 0:
                    frame = frame[:, :-pan_x] if pan_x < w else frame
                
                return frame
            
            return clip.time_transform(pan_effect)
        except Exception as e:
            print(f"Error applying pan right: {str(e)}")
            return clip
    
    def _apply_zoom_in(self, clip):
        """Zoom in effect"""
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
        """Zoom out effect"""
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
    
    def _apply_enhanced_transition(self, clip, transition, index, total_clips):
        """Apply enhanced transitions between clips"""
        try:
            if transition == 'fade':
                if index == 0:
                    return clip.with_effects([fadein(0.5)  # First clip fades in
                elif index == total_clips - 1:
                    return clip.with_effects([fadeout(0.5)  # Last clip fades out
                else:
                    return clip.with_effects([fadein(0.3).with_effects([fadeout(0.3)  # Middle clips fade in/out
            elif transition == 'slide_left':
                return clip.with_position(lambda t: (t * 100, 0)).with_effects([fadein(0.3).with_effects([fadeout(0.3)
            elif transition == 'slide_right':
                return clip.with_position(lambda t: (-t * 100, 0)).with_effects([fadein(0.3).with_effects([fadeout(0.3)
            elif transition == 'zoom_in':
                return clip.with_effects([fadein(0.3).with_effects([fadeout(0.3)
            elif transition == 'zoom_out':
                return clip.with_effects([fadein(0.3).with_effects([fadeout(0.3)
            elif transition == 'crossfade':
                return clip.with_effects([fadein(0.5).with_effects([fadeout(0.5)
            else:
                return clip.with_effects([fadein(0.3).with_effects([fadeout(0.3)
        except Exception as e:
            print(f"Error applying transition {transition}: {str(e)}")
            return clip
    
    def _add_enhanced_background_music(self, video, music_style):
        """Add enhanced background music to video"""
        try:
            print(f"Adding {music_style} background music...")
            
            # Generate music based on style
            music = self.music_service.get_background_music(music_style, video.duration)
            
            # Set volume (not too loud) - use correct MoviePy method
            music = music.with_volume_scaled(0.3)
            
            # Add fade in/out to music
            music = music.with_effects([fadein(1).with_effects([fadeout(1)
            
            return video.set_audio(music)
        except Exception as e:
            print(f"Error adding enhanced background music: {str(e)}")
            # Return video without audio if music fails
            return video
    
    def create_social_media_variants(self, video_path, formats=['16:9', '9:16', '1:1']):
        """Create different aspect ratios for social media"""
        variants = {}
        
        for format_type in formats:
            try:
                if format_type == '16:9':
                    # Already in 16:9
                    variants['16:9'] = video_path
                elif format_type == '9:16':
                    # Vertical format for Instagram Stories, TikTok
                    clip = VideoFileClip(video_path)
                    # Crop to 9:16 aspect ratio
                    new_clip = clip.crop(x_center=clip.w/2, y_center=clip.h/2, width=clip.h*9/16, height=clip.h)
                    output_path = video_path.replace('.mp4', '_9x16.mp4')
                    new_clip.write_videofile(output_path)
                    variants['9:16'] = output_path
                    new_clip.close()
                elif format_type == '1:1':
                    # Square format for Instagram posts
                    clip = VideoFileClip(video_path)
                    # Crop to square
                    size = min(clip.w, clip.h)
                    new_clip = clip.crop(x_center=clip.w/2, y_center=clip.h/2, width=size, height=size)
                    output_path = video_path.replace('.mp4', '_1x1.mp4')
                    new_clip.write_videofile(output_path)
                    variants['1:1'] = output_path
                    new_clip.close()
            except Exception as e:
                print(f"Error creating {format_type} variant: {str(e)}")
        
        return variants

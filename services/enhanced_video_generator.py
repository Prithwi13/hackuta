#!/usr/bin/env python3
"""
Enhanced video generator with vector RAG and improved effects
"""

import os
import numpy as np
from moviepy.editor import ImageClip, ColorClip, concatenate_videoclips, CompositeVideoClip, AudioClip
from PIL import Image
from typing import List, Dict, Any
from config import DEFAULT_VIDEO_WIDTH, DEFAULT_VIDEO_HEIGHT, DEFAULT_VIDEO_FPS, OUTPUT_DIR
from services.enhanced_music_service import EnhancedMusicService

class EnhancedVideoGenerator:
    def __init__(self):
        """Initialize enhanced video generator"""
        self.music_service = EnhancedMusicService(use_musicgen=True, use_external_api=False)
        print("Enhanced video generator initialized!")

    def create_video(self, photo_paths: List[str], context: str, video_plan: Dict[str, Any], output_filename: str = "enhanced_memory.mp4") -> str:
        """Create enhanced video with vector RAG effects and transitions"""
        try:
            print(f"Creating enhanced video with {len(photo_paths)} photos")
            print(f"Video plan: {video_plan}")
            
            # Extract plan details
            effects = video_plan.get('effects', ['static'] * len(photo_paths))
            transitions = video_plan.get('transitions', ['crossfade'] * len(photo_paths))
            music_style = video_plan.get('music_style', 'nostalgic')
            duration_per_photo = video_plan.get('duration_per_photo', 4)
            
            # Create enhanced clips
            clips = []
            total_duration = 0
            
            for i, photo_path in enumerate(photo_paths):
                effect = effects[i] if i < len(effects) else 'static'
                transition = transitions[i] if i < len(transitions) else 'crossfade'
                
                print(f"Processing photo {i+1}/{len(photo_paths)}: {os.path.basename(photo_path)}")
                print(f"Effect: {effect}, Transition: {transition}")
                
                clip = self._create_enhanced_clip(photo_path, duration_per_photo, effect)
                clips.append(clip)
                total_duration += duration_per_photo
            
            # Apply transitions and concatenate
            final_video = self._apply_transitions(clips, transitions)
            final_video = final_video.set_fps(DEFAULT_VIDEO_FPS)
            
            # Add enhanced background music
            music_clip = self.music_service.get_background_music(
                music_style, 
                total_duration, 
                context
            )
            
            if music_clip:
                # Adjust volume and add to video
                music_clip = music_clip.volumex(0.4)  # 40% volume
                final_video = final_video.set_audio(music_clip)
            
            # Write final video
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            print(f"Writing enhanced video to: {output_path}")
            
            final_video.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                fps=DEFAULT_VIDEO_FPS,
                bitrate='5000k',  # High quality
                temp_audiofile='temp-audio.m4a',
                remove_temp=True
            )
            
            print(f"Enhanced video created successfully: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error creating enhanced video: {str(e)}")
            return None

    def _create_enhanced_clip(self, photo_path: str, duration: float, effect: str) -> ImageClip:
        """Create enhanced clip with sophisticated effects"""
        try:
            # Load and process image
            img = Image.open(photo_path)
            clip = ImageClip(photo_path, duration=duration)
            
            # Resize and center
            clip = self._resize_and_center_clip(clip)
            
            # Apply enhanced effects
            if effect == 'ken_burns_zoom_in':
                clip = self._apply_ken_burns_zoom_in(clip, duration)
            elif effect == 'ken_burns_zoom_out':
                clip = self._apply_ken_burns_zoom_out(clip, duration)
            elif effect == 'pan_left':
                clip = self._apply_pan_left(clip, duration)
            elif effect == 'pan_right':
                clip = self._apply_pan_right(clip, duration)
            elif effect == 'zoom_in_center':
                clip = self._apply_zoom_in_center(clip, duration)
            elif effect == 'zoom_out_center':
                clip = self._apply_zoom_out_center(clip, duration)
            elif effect == 'static':
                pass  # No effect
            
            return clip
            
        except Exception as e:
            print(f"Error creating enhanced clip: {str(e)}")
            # Return fallback clip
            return ColorClip(size=(DEFAULT_VIDEO_WIDTH, DEFAULT_VIDEO_HEIGHT), color=(0, 0, 0), duration=duration)

    def _resize_and_center_clip(self, clip: ImageClip) -> ImageClip:
        """Resize and center clip while maintaining aspect ratio"""
        try:
            # Calculate target size
            aspect_ratio = clip.w / clip.h
            video_aspect_ratio = DEFAULT_VIDEO_WIDTH / DEFAULT_VIDEO_HEIGHT
            
            if aspect_ratio > video_aspect_ratio:
                # Image is wider than video
                new_width = DEFAULT_VIDEO_WIDTH
                new_height = int(DEFAULT_VIDEO_WIDTH / aspect_ratio)
            else:
                # Image is taller than video
                new_height = DEFAULT_VIDEO_HEIGHT
                new_width = int(DEFAULT_VIDEO_HEIGHT * aspect_ratio)
            
            # Resize clip
            clip = clip.resize(newsize=(new_width, new_height))
            
            # Center the clip
            x_center = (DEFAULT_VIDEO_WIDTH - new_width) // 2
            y_center = (DEFAULT_VIDEO_HEIGHT - new_height) // 2
            clip = clip.set_position((x_center, y_center))
            
            return clip
            
        except Exception as e:
            print(f"Error resizing clip: {str(e)}")
            return clip

    def _apply_ken_burns_zoom_in(self, clip: ImageClip, duration: float) -> ImageClip:
        """Apply Ken Burns zoom in effect"""
        try:
            # Start with larger scale, zoom in
            def zoom_func(t):
                scale = 1.1 - 0.1 * (t / duration)
                return scale
            
            clip = clip.resize(zoom_func)
            return clip
        except Exception as e:
            print(f"Error applying Ken Burns zoom in: {str(e)}")
            return clip

    def _apply_ken_burns_zoom_out(self, clip: ImageClip, duration: float) -> ImageClip:
        """Apply Ken Burns zoom out effect"""
        try:
            # Start with smaller scale, zoom out
            def zoom_func(t):
                scale = 0.9 + 0.1 * (t / duration)
                return scale
            
            clip = clip.resize(zoom_func)
            return clip
        except Exception as e:
            print(f"Error applying Ken Burns zoom out: {str(e)}")
            return clip

    def _apply_pan_left(self, clip: ImageClip, duration: float) -> ImageClip:
        """Apply pan left effect"""
        try:
            def position_func(t):
                # Start from right, move to left
                x_offset = (1 - t / duration) * (clip.w - DEFAULT_VIDEO_WIDTH)
                return (x_offset, 'center')
            
            clip = clip.set_position(position_func)
            return clip
        except Exception as e:
            print(f"Error applying pan left: {str(e)}")
            return clip

    def _apply_pan_right(self, clip: ImageClip, duration: float) -> ImageClip:
        """Apply pan right effect"""
        try:
            def position_func(t):
                # Start from left, move to right
                x_offset = (t / duration) * (DEFAULT_VIDEO_WIDTH - clip.w)
                return (x_offset, 'center')
            
            clip = clip.set_position(position_func)
            return clip
        except Exception as e:
            print(f"Error applying pan right: {str(e)}")
            return clip

    def _apply_zoom_in_center(self, clip: ImageClip, duration: float) -> ImageClip:
        """Apply zoom in from center"""
        try:
            def zoom_func(t):
                scale = 1.0 + 0.2 * (t / duration)
                return scale
            
            clip = clip.resize(zoom_func)
            return clip
        except Exception as e:
            print(f"Error applying zoom in center: {str(e)}")
            return clip

    def _apply_zoom_out_center(self, clip: ImageClip, duration: float) -> ImageClip:
        """Apply zoom out from center"""
        try:
            def zoom_func(t):
                scale = 1.2 - 0.2 * (t / duration)
                return scale
            
            clip = clip.resize(zoom_func)
            return clip
        except Exception as e:
            print(f"Error applying zoom out center: {str(e)}")
            return clip

    def _apply_transitions(self, clips: List[ImageClip], transitions: List[str]) -> ImageClip:
        """Apply sophisticated transitions between clips"""
        try:
            if len(clips) == 1:
                return clips[0]
            
            # For now, use simple concatenation with crossfade
            # More sophisticated transitions would require overlapping clips
            final_clips = []
            
            for i, clip in enumerate(clips):
                # Apply fade in/out based on transition
                transition = transitions[i] if i < len(transitions) else 'crossfade'
                
                if transition == 'fade_in' and i == 0:
                    clip = clip.fadein(1.0)
                elif transition == 'fade_out' and i == len(clips) - 1:
                    clip = clip.fadeout(1.0)
                elif transition in ['crossfade', 'dissolve']:
                    # Apply crossfade effect
                    if i > 0:
                        clip = clip.fadein(0.5)
                    if i < len(clips) - 1:
                        clip = clip.fadeout(0.5)
                
                final_clips.append(clip)
            
            # Concatenate with crossfade
            return concatenate_videoclips(final_clips, method="compose")
            
        except Exception as e:
            print(f"Error applying transitions: {str(e)}")
            # Fallback to simple concatenation
            return concatenate_videoclips(clips)

    def get_video_info(self, video_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Get information about the video plan"""
        return {
            'effects': video_plan.get('effects', []),
            'transitions': video_plan.get('transitions', []),
            'music_style': video_plan.get('music_style', 'nostalgic'),
            'duration_per_photo': video_plan.get('duration_per_photo', 4),
            'total_duration': len(video_plan.get('effects', [])) * video_plan.get('duration_per_photo', 4),
            'video_style': video_plan.get('video_style', 'professional'),
            'mood': video_plan.get('mood', 'emotional')
        }

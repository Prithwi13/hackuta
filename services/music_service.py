import os
import numpy as np
from moviepy import AudioClip, CompositeAudioClip
import random

class MusicService:
    def __init__(self):
        self.music_folder = 'static/music'
        self.sample_music = {
            'upbeat': self._create_upbeat_music,
            'nostalgic': self._create_nostalgic_music,
            'romantic': self._create_romantic_music,
            'energetic': self._create_energetic_music,
            'calm': self._create_calm_music
        }
    
    def get_background_music(self, music_style, duration):
        """Generate background music based on style and duration"""
        try:
            if music_style in self.sample_music:
                return self.sample_music[music_style](duration)
            else:
                return self._create_default_music(duration)
        except Exception as e:
            print(f"Error generating music: {str(e)}")
            return self._create_default_music(duration)
    
    def _create_upbeat_music(self, duration):
        """Create upbeat, happy music"""
        def make_frame(t):
            # Create a simple melody with multiple frequencies
            freq1 = 440  # A4 note
            freq2 = 554  # C#5 note
            freq3 = 659  # E5 note
            
            # Create a simple chord progression
            wave1 = np.sin(2 * np.pi * freq1 * t) * 0.3
            wave2 = np.sin(2 * np.pi * freq2 * t) * 0.2
            wave3 = np.sin(2 * np.pi * freq3 * t) * 0.2
            
            # Add some rhythm
            rhythm = np.sin(2 * np.pi * 2 * t) * 0.1
            
            return wave1 + wave2 + wave3 + rhythm
        
        return AudioClip(make_frame, duration=duration)
    
    def _create_nostalgic_music(self, duration):
        """Create nostalgic, emotional music"""
        def make_frame(t):
            # Slower, more emotional frequencies
            freq1 = 330  # E4 note
            freq2 = 415  # G#4 note
            freq3 = 523  # C5 note
            
            # Slower tempo
            wave1 = np.sin(2 * np.pi * freq1 * t * 0.5) * 0.4
            wave2 = np.sin(2 * np.pi * freq2 * t * 0.5) * 0.3
            wave3 = np.sin(2 * np.pi * freq3 * t * 0.5) * 0.2
            
            # Add some vibrato
            vibrato = np.sin(2 * np.pi * 5 * t) * 0.1
            
            return wave1 + wave2 + wave3 + vibrato
    
        return AudioClip(make_frame, duration=duration)
    
    def _create_romantic_music(self, duration):
        """Create romantic, soft music"""
        def make_frame(t):
            # Soft, romantic frequencies
            freq1 = 392  # G4 note
            freq2 = 494  # B4 note
            freq3 = 587  # D5 note
            
            # Soft attack
            envelope = np.exp(-t * 0.1) if t < 1 else 0.5
            
            wave1 = np.sin(2 * np.pi * freq1 * t) * 0.3 * envelope
            wave2 = np.sin(2 * np.pi * freq2 * t) * 0.2 * envelope
            wave3 = np.sin(2 * np.pi * freq3 * t) * 0.2 * envelope
            
            return wave1 + wave2 + wave3
    
        return AudioClip(make_frame, duration=duration)
    
    def _create_energetic_music(self, duration):
        """Create energetic, fast-paced music"""
        def make_frame(t):
            # Higher frequencies for energy
            freq1 = 523  # C5 note
            freq2 = 659  # E5 note
            freq3 = 784  # G5 note
            
            # Fast tempo
            wave1 = np.sin(2 * np.pi * freq1 * t * 2) * 0.3
            wave2 = np.sin(2 * np.pi * freq2 * t * 2) * 0.2
            wave3 = np.sin(2 * np.pi * freq3 * t * 2) * 0.2
            
            # Add some percussion-like rhythm
            percussion = np.sin(2 * np.pi * 4 * t) * 0.1
            
            return wave1 + wave2 + wave3 + percussion
    
        return AudioClip(make_frame, duration=duration)
    
    def _create_calm_music(self, duration):
        """Create calm, peaceful music"""
        def make_frame(t):
            # Low, peaceful frequencies
            freq1 = 220  # A3 note
            freq2 = 277  # C#4 note
            freq3 = 330  # E4 note
            
            # Very slow tempo
            wave1 = np.sin(2 * np.pi * freq1 * t * 0.3) * 0.4
            wave2 = np.sin(2 * np.pi * freq2 * t * 0.3) * 0.3
            wave3 = np.sin(2 * np.pi * freq3 * t * 0.3) * 0.2
            
            return wave1 + wave2 + wave3
    
        return AudioClip(make_frame, duration=duration)
    
    def _create_default_music(self, duration):
        """Create default background music"""
        def make_frame(t):
            # Simple, pleasant melody
            freq = 440  # A4 note
            wave = np.sin(2 * np.pi * freq * t) * 0.2
            return wave
    
        return AudioClip(make_frame, duration=duration)

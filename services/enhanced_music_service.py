#!/usr/bin/env python3
"""
Enhanced music service with MusicGen and external audio APIs
"""

import os
import numpy as np
import torch
from moviepy.editor import AudioClip
from typing import Dict, Any, Optional
import requests
import json
from datetime import datetime

class EnhancedMusicService:
    def __init__(self, use_musicgen: bool = True, use_external_api: bool = False):
        """Initialize enhanced music service"""
        self.use_musicgen = use_musicgen
        self.use_external_api = use_external_api
        
        # MusicGen model (if available)
        self.musicgen_model = None
        self.musicgen_processor = None
        
        if use_musicgen:
            try:
                from transformers import MusicgenForConditionalGeneration, AutoProcessor
                print("Loading MusicGen model...")
                self.musicgen_model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
                self.musicgen_processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
                print("MusicGen model loaded successfully!")
            except Exception as e:
                print(f"Could not load MusicGen: {str(e)}")
                self.use_musicgen = False
        
        # External API configuration
        self.external_api_key = os.getenv("AUDIO_API_KEY")
        self.external_api_url = "https://api.example.com/audio"  # Replace with actual API
        
        # Music style configurations
        self.music_styles = {
            'nostalgic': {
                'description': 'Warm, sentimental music for memories',
                'prompt': 'nostalgic piano melody, warm strings, emotional, sentimental',
                'tempo': 80,
                'key': 'C major',
                'instruments': ['piano', 'strings', 'soft_synth']
            },
            'upbeat': {
                'description': 'Energetic, positive music for celebrations',
                'prompt': 'upbeat pop music, energetic drums, bright synthesizer, celebratory',
                'tempo': 120,
                'key': 'G major',
                'instruments': ['drums', 'bass', 'synthesizer']
            },
            'romantic': {
                'description': 'Soft, romantic music for intimate moments',
                'prompt': 'romantic piano ballad, soft strings, intimate, loving',
                'tempo': 70,
                'key': 'F major',
                'instruments': ['piano', 'strings', 'soft_synth']
            },
            'energetic': {
                'description': 'High-energy music for action and excitement',
                'prompt': 'energetic rock music, fast drums, electric guitar, exciting',
                'tempo': 140,
                'key': 'E major',
                'instruments': ['drums', 'electric_guitar', 'bass']
            },
            'calm': {
                'description': 'Peaceful, relaxing music for serene moments',
                'prompt': 'calm ambient music, soft piano, peaceful, relaxing',
                'tempo': 60,
                'key': 'A major',
                'instruments': ['piano', 'soft_synth', 'ambient']
            },
            'dramatic': {
                'description': 'Intense, dramatic music for powerful moments',
                'prompt': 'dramatic orchestral music, intense strings, powerful, cinematic',
                'tempo': 100,
                'key': 'D minor',
                'instruments': ['orchestra', 'strings', 'piano']
            }
        }

    def get_background_music(self, style: str, duration: float, context: str = "") -> AudioClip:
        """Generate or retrieve background music"""
        try:
            if self.use_musicgen and self.musicgen_model:
                return self._generate_musicgen_audio(style, duration, context)
            elif self.use_external_api and self.external_api_key:
                return self._fetch_external_audio(style, duration, context)
            else:
                return self._generate_synthetic_audio(style, duration)
        except Exception as e:
            print(f"Error generating music: {str(e)}")
            return self._generate_synthetic_audio(style, duration)

    def _generate_musicgen_audio(self, style: str, duration: float, context: str) -> AudioClip:
        """Generate audio using MusicGen model"""
        try:
            style_config = self.music_styles.get(style, self.music_styles['calm'])
            
            # Create enhanced prompt
            prompt = f"{style_config['prompt']}"
            if context:
                prompt += f", {context}"
            
            # Generate audio
            inputs = self.musicgen_processor(
                text=[prompt],
                padding=True,
                return_tensors="pt"
            )
            
            with torch.no_grad():
                audio_values = self.musicgen_model.generate(
                    **inputs,
                    max_new_tokens=int(duration * 50),  # Approximate tokens for duration
                    do_sample=True,
                    guidance_scale=3.0
                )
            
            # Convert to numpy array
            audio_array = audio_values[0].cpu().numpy()
            
            # Create AudioClip
            def make_frame(t):
                if isinstance(t, np.ndarray):
                    t = t[0] if len(t) > 0 else 0
                
                # Ensure t is within bounds
                t = max(0, min(t, duration))
                sample_idx = int(t * 22050)  # 22050 Hz sample rate
                
                if sample_idx < len(audio_array):
                    return audio_array[sample_idx]
                else:
                    return 0
            
            return AudioClip(make_frame, duration=duration, fps=22050)
            
        except Exception as e:
            print(f"Error with MusicGen: {str(e)}")
            return self._generate_synthetic_audio(style, duration)

    def _fetch_external_audio(self, style: str, duration: float, context: str) -> AudioClip:
        """Fetch audio from external API"""
        try:
            style_config = self.music_styles.get(style, self.music_styles['calm'])
            
            payload = {
                'style': style,
                'duration': duration,
                'context': context,
                'tempo': style_config['tempo'],
                'key': style_config['key'],
                'instruments': style_config['instruments']
            }
            
            headers = {
                'Authorization': f'Bearer {self.external_api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                self.external_api_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                # Process audio data from API
                audio_data = response.json()
                # Convert to AudioClip (implementation depends on API response format)
                return self._process_external_audio(audio_data, duration)
            else:
                print(f"External API error: {response.status_code}")
                return self._generate_synthetic_audio(style, duration)
                
        except Exception as e:
            print(f"Error fetching external audio: {str(e)}")
            return self._generate_synthetic_audio(style, duration)

    def _process_external_audio(self, audio_data: Dict, duration: float) -> AudioClip:
        """Process audio data from external API"""
        # This would depend on the specific API response format
        # For now, fall back to synthetic audio
        return self._generate_synthetic_audio('calm', duration)

    def _generate_synthetic_audio(self, style: str, duration: float) -> AudioClip:
        """Generate synthetic audio as fallback"""
        style_config = self.music_styles.get(style, self.music_styles['calm'])
        
        def make_frame(t):
            # Handle both single values and arrays
            if hasattr(t, '__len__') and len(t) > 1:
                t = t[0] if len(t) > 0 else 0
            
            # Generate enhanced synthetic audio based on style
            if style == 'nostalgic':
                # Nostalgic melody with warm tones
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
        
        return AudioClip(make_frame, duration=duration, fps=44100)

    def get_music_info(self, style: str) -> Dict[str, Any]:
        """Get information about a music style"""
        return self.music_styles.get(style, self.music_styles['calm'])

    def list_available_styles(self) -> List[str]:
        """List all available music styles"""
        return list(self.music_styles.keys())

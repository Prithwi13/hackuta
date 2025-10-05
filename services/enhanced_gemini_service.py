#!/usr/bin/env python3
"""
Enhanced Gemini service with proper API integration and plan parsing
"""

import os
import json
import google.generativeai as genai
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
import re

load_dotenv()

class EnhancedGeminiService:
    def __init__(self, api_key: str = None):
        """Initialize enhanced Gemini service with proper API key handling"""
        self.api_key = api_key if api_key else os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            print("Warning: GEMINI_API_KEY not found. Using fallback planning.")
            self.model = None
            self.available = False
        else:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.available = True
                print("Enhanced Gemini service initialized successfully!")
            except Exception as e:
                print(f"Error initializing Gemini: {str(e)}")
                self.model = None
                self.available = False

    def plan_video_with_enhanced_context(self, photo_paths: List[str], context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Plan video using enhanced context with proper Gemini integration"""
        try:
            if not self.available or not self.model:
                return self._get_fallback_plan(len(photo_paths), context_data)
            
            # Extract enhanced context
            overall_context = context_data.get('overall_context', '')
            themes = context_data.get('themes', [])
            entities = context_data.get('entities', [])
            scene_classifications = context_data.get('scene_classifications', [])
            
            # Create comprehensive prompt
            prompt = self._create_enhanced_prompt(photo_paths, overall_context, themes, entities, scene_classifications)
            
            # Generate response from Gemini
            response = self.model.generate_content(prompt)
            plan_text = response.text
            
            print(f"Gemini Enhanced Plan: {plan_text}")
            
            # Parse and validate the response
            return self._parse_and_validate_plan(plan_text, len(photo_paths), context_data)
            
        except Exception as e:
            print(f"Error in enhanced Gemini planning: {str(e)}")
            return self._get_fallback_plan(len(photo_paths), context_data)

    def _create_enhanced_prompt(self, photo_paths: List[str], context: str, themes: List[str], 
                              entities: List[str], scenes: List[str]) -> str:
        """Create comprehensive prompt for Gemini"""
        photo_descriptions = "\n".join([f"- Photo {i+1}: {os.path.basename(p)}" for i, p in enumerate(photo_paths)])
        
        prompt = f"""
You are an expert video editor AI with access to advanced video production techniques. 
Create a detailed video plan for a professional memory video based on the following information:

PHOTOS:
{photo_descriptions}

CONTEXT ANALYSIS:
- Overall Context: {context}
- Identified Themes: {', '.join(themes) if themes else 'None detected'}
- Key Entities: {', '.join(entities[:10]) if entities else 'None detected'}
- Scene Classifications: {', '.join(scenes[:5]) if scenes else 'None detected'}

AVAILABLE EFFECTS:
- ken_burns_zoom_in: Slow zoom in for intimate moments
- ken_burns_zoom_out: Slow zoom out for revealing context
- pan_left: Horizontal pan from right to left
- pan_right: Horizontal pan from left to right
- zoom_in_center: Zoom in from center point
- zoom_out_center: Zoom out from center point
- static: No movement, clean and stable

AVAILABLE TRANSITIONS:
- fade_in: Smooth fade in from black
- fade_out: Smooth fade out to black
- crossfade: Smooth blend between clips
- slide_left: Slide in from right, slide out to left
- slide_right: Slide in from left, slide out to right
- zoom_transition: Zoom in/out transition effect
- dissolve: Soft dissolve between clips

AVAILABLE MUSIC STYLES:
- nostalgic: Warm, sentimental music for memories
- upbeat: Energetic, positive music for celebrations
- romantic: Soft, romantic music for intimate moments
- energetic: High-energy music for action and excitement
- calm: Peaceful, relaxing music for serene moments
- dramatic: Intense, dramatic music for powerful moments

TASK:
Create a professional video plan that matches the content and mood of the photos. 
Consider the themes, entities, and scene classifications to make intelligent choices.

Provide your response in the following JSON format:
{{
    "sequence": [0, 1, 2, 3, 4],
    "effects": ["ken_burns_zoom_in", "pan_left", "static", "zoom_out_center", "ken_burns_zoom_out"],
    "transitions": ["fade_in", "crossfade", "slide_left", "dissolve", "fade_out"],
    "music_style": "nostalgic",
    "duration_per_photo": 4,
    "video_style": "cinematic and emotional",
    "mood": "warm and sentimental",
    "reasoning": "Brief explanation of your choices"
}}

Ensure all arrays have exactly {len(photo_paths)} elements and use only the available effects, transitions, and music styles listed above.
"""
        return prompt

    def _parse_and_validate_plan(self, plan_text: str, photo_count: int, context_data: Dict) -> Dict[str, Any]:
        """Parse and validate Gemini response"""
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', plan_text, re.DOTALL)
            if json_match:
                plan_json = json.loads(json_match.group())
            else:
                # Try to parse the entire text as JSON
                plan_json = json.loads(plan_text)
            
            # Validate and fix the plan
            validated_plan = self._validate_plan(plan_json, photo_count)
            
            # Add context information
            validated_plan['context_info'] = {
                'themes': context_data.get('themes', []),
                'entities': context_data.get('entities', []),
                'scenes': context_data.get('scene_classifications', [])
            }
            
            return validated_plan
            
        except json.JSONDecodeError as e:
            print(f"Error parsing Gemini JSON: {str(e)}")
            return self._get_fallback_plan(photo_count, context_data)
        except Exception as e:
            print(f"Error validating plan: {str(e)}")
            return self._get_fallback_plan(photo_count, context_data)

    def _validate_plan(self, plan: Dict[str, Any], photo_count: int) -> Dict[str, Any]:
        """Validate and fix the video plan"""
        # Valid options
        valid_effects = [
            'ken_burns_zoom_in', 'ken_burns_zoom_out', 'pan_left', 'pan_right',
            'zoom_in_center', 'zoom_out_center', 'static'
        ]
        valid_transitions = [
            'fade_in', 'fade_out', 'crossfade', 'slide_left', 'slide_right',
            'zoom_transition', 'dissolve'
        ]
        valid_music = [
            'nostalgic', 'upbeat', 'romantic', 'energetic', 'calm', 'dramatic'
        ]
        
        # Ensure sequence exists and is correct length
        if 'sequence' not in plan:
            plan['sequence'] = list(range(photo_count))
        elif len(plan['sequence']) != photo_count:
            plan['sequence'] = list(range(photo_count))
        
        # Validate and fix effects
        if 'effects' not in plan or len(plan['effects']) != photo_count:
            plan['effects'] = ['static'] * photo_count
        else:
            plan['effects'] = [
                effect if effect in valid_effects else 'static'
                for effect in plan['effects']
            ]
        
        # Validate and fix transitions
        if 'transitions' not in plan or len(plan['transitions']) != photo_count:
            plan['transitions'] = ['crossfade'] * photo_count
        else:
            plan['transitions'] = [
                transition if transition in valid_transitions else 'crossfade'
                for transition in plan['transitions']
            ]
        
        # Validate music style
        if 'music_style' not in plan or plan['music_style'] not in valid_music:
            plan['music_style'] = 'nostalgic'
        
        # Validate duration
        if 'duration_per_photo' not in plan or not isinstance(plan['duration_per_photo'], (int, float)):
            plan['duration_per_photo'] = 4
        
        # Ensure other required fields
        plan['video_style'] = plan.get('video_style', 'cinematic and professional')
        plan['mood'] = plan.get('mood', 'warm and emotional')
        plan['reasoning'] = plan.get('reasoning', 'AI-generated plan based on photo analysis')
        
        return plan

    def _get_fallback_plan(self, photo_count: int, context_data: Dict) -> Dict[str, Any]:
        """Get fallback plan when Gemini is not available"""
        import random
        
        # Use context to make better fallback choices
        themes = context_data.get('themes', [])
        entities = context_data.get('entities', [])
        
        # Choose music style based on themes
        if 'family' in themes or 'romantic' in themes:
            music_style = 'nostalgic'
        elif 'celebration' in themes or 'party' in themes:
            music_style = 'upbeat'
        elif 'travel' in themes or 'adventure' in themes:
            music_style = 'energetic'
        elif 'nature' in themes or 'calm' in themes:
            music_style = 'calm'
        elif 'dramatic' in themes or 'important' in themes:
            music_style = 'dramatic'
        else:
            music_style = 'nostalgic'
        
        # Generate varied effects
        effects = []
        effect_options = ['ken_burns_zoom_in', 'ken_burns_zoom_out', 'pan_left', 'pan_right', 'zoom_in_center', 'zoom_out_center', 'static']
        for i in range(photo_count):
            effects.append(effect_options[i % len(effect_options)])
        
        # Generate varied transitions
        transitions = []
        transition_options = ['fade_in', 'crossfade', 'slide_left', 'slide_right', 'zoom_transition', 'dissolve', 'fade_out']
        for i in range(photo_count):
            transitions.append(transition_options[i % len(transition_options)])
        
        return {
            'sequence': list(range(photo_count)),
            'effects': effects,
            'transitions': transitions,
            'music_style': music_style,
            'duration_per_photo': 4,
            'video_style': 'professional and cinematic',
            'mood': 'engaging and emotional',
            'reasoning': 'Fallback plan based on context analysis',
            'context_info': {
                'themes': themes,
                'entities': entities,
                'scenes': context_data.get('scene_classifications', [])
            }
        }

    def test_connection(self) -> bool:
        """Test Gemini API connection"""
        if not self.available:
            return False
        
        try:
            test_prompt = "Generate a simple test response."
            response = self.model.generate_content(test_prompt)
            return response.text is not None
        except Exception as e:
            print(f"Gemini connection test failed: {str(e)}")
            return False

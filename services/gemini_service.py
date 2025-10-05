import google.generativeai as genai
from config import GEMINI_API_KEY
import json

class GeminiService:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro-vision')
    
    def plan_video(self, photo_paths, context):
        """
        Use Gemini to analyze photos and generate video planning recommendations
        """
        try:
            # Prepare the prompt for Gemini
            prompt = f"""
            Analyze these photos and create a video plan with the following context:
            
            Context: {context.get('overall_context', 'No context available')}
            
            Individual photo descriptions:
            {self._format_photo_descriptions(context.get('individual_captions', []))}
            
            Please provide a JSON response with:
            1. Suggested photo sequence (reorder if needed)
            2. Recommended transitions between photos
            3. Suggested background music style
            4. Recommended video duration per photo
            5. Overall video style/theme
            6. Any special effects or enhancements
            
            Format your response as JSON with these keys:
            - sequence: array of photo indices in recommended order
            - transitions: array of transition types for each photo
            - music_style: string describing recommended music
            - duration_per_photo: number in seconds
            - video_style: string describing overall style
            - special_effects: array of suggested effects
            """
            
            # For now, return a default plan since we need to handle image inputs properly
            return self._get_default_plan(len(photo_paths))
            
        except Exception as e:
            print(f"Error in Gemini video planning: {str(e)}")
            return self._get_default_plan(len(photo_paths))
    
    def _format_photo_descriptions(self, captions):
        """Format photo descriptions for Gemini prompt"""
        formatted = []
        for i, caption in enumerate(captions):
            formatted.append(f"Photo {i+1}: {caption.get('caption', 'No description')}")
        return "\n".join(formatted)
    
    def _get_default_plan(self, photo_count):
        """Get default video plan when Gemini is not available"""
        import random
        
        # Random music styles
        music_styles = ['nostalgic', 'upbeat', 'romantic', 'energetic', 'calm']
        music_style = random.choice(music_styles)
        
        # Generate varied transitions
        transitions = []
        transition_types = ['fade', 'slide_left', 'slide_right', 'zoom_in', 'zoom_out', 'crossfade']
        for i in range(photo_count):
            if i == 0:
                transitions.append('fade')
            elif i == photo_count - 1:
                transitions.append('fade')
            else:
                transitions.append(random.choice(transition_types))
        
        return {
            'sequence': list(range(photo_count)),
            'transitions': transitions,
            'music_style': music_style,
            'duration_per_photo': 3,
            'video_style': 'modern and dynamic',
            'special_effects': ['ken_burns_zoom', 'pan_effects', 'zoom_effects']
        }
    
    def analyze_photos_with_gemini(self, photo_paths):
        """
        Analyze photos using Gemini's vision capabilities
        """
        try:
            # This would require proper image handling with Gemini
            # For now, return basic analysis
            analysis = {
                'emotions': ['joy', 'nostalgia'],
                'themes': ['memories', 'celebration'],
                'recommended_style': 'warm and personal',
                'suggested_music': 'acoustic and uplifting'
            }
            return analysis
        except Exception as e:
            print(f"Error in Gemini photo analysis: {str(e)}")
            return {'error': 'Unable to analyze photos'}




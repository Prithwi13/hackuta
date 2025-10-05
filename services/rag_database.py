import json
import os
from typing import List, Dict, Any

class RAGDatabase:
    def __init__(self):
        self.database_file = "rag_database.json"
        self.database = self._load_database()
    
    def _load_database(self):
        """Load or create the RAG database"""
        if os.path.exists(self.database_file):
            with open(self.database_file, 'r') as f:
                return json.load(f)
        else:
            # Create initial database
            database = {
                "video_effects": self._get_video_effects(),
                "transitions": self._get_transitions(),
                "music_styles": self._get_music_styles(),
                "video_templates": self._get_video_templates()
            }
            self._save_database(database)
            return database
    
    def _save_database(self, database):
        """Save database to file"""
        with open(self.database_file, 'w') as f:
            json.dump(database, f, indent=2)
    
    def _get_video_effects(self):
        """Get sample video effects"""
        return [
            {
                "name": "ken_burns_zoom_in",
                "description": "Slow zoom in effect, creates depth and focus",
                "use_case": "Portrait photos, close-up shots, emotional moments",
                "technical": "Gradual scale increase from 1.0 to 1.2 over duration",
                "mood": "intimate, emotional, focused"
            },
            {
                "name": "ken_burns_zoom_out", 
                "description": "Slow zoom out effect, reveals more context",
                "use_case": "Landscape photos, group shots, establishing shots",
                "technical": "Gradual scale decrease from 1.2 to 1.0 over duration",
                "mood": "expansive, revealing, contextual"
            },
            {
                "name": "pan_left",
                "description": "Horizontal pan from right to left",
                "use_case": "Wide photos, panoramic shots, travel photos",
                "technical": "Horizontal movement from right edge to left edge",
                "mood": "dynamic, cinematic, storytelling"
            },
            {
                "name": "pan_right",
                "description": "Horizontal pan from left to right", 
                "use_case": "Wide photos, panoramic shots, travel photos",
                "technical": "Horizontal movement from left edge to right edge",
                "mood": "dynamic, cinematic, storytelling"
            },
            {
                "name": "static",
                "description": "No movement, clean and stable",
                "use_case": "Portrait photos, detailed shots, important moments",
                "technical": "No transformation applied",
                "mood": "stable, focused, important"
            },
            {
                "name": "zoom_in_center",
                "description": "Zoom in from center point",
                "use_case": "Portrait photos, detailed shots, emotional moments",
                "technical": "Scale increase from center point",
                "mood": "intimate, emotional, focused"
            },
            {
                "name": "zoom_out_center",
                "description": "Zoom out from center point",
                "use_case": "Group photos, landscape shots, context revealing",
                "technical": "Scale decrease from center point",
                "mood": "expansive, revealing, contextual"
            }
        ]
    
    def _get_transitions(self):
        """Get sample transitions"""
        return [
            {
                "name": "fade_in",
                "description": "Smooth fade in from black",
                "use_case": "Opening shots, dramatic moments, emotional scenes",
                "technical": "Opacity transition from 0 to 1 over 1 second",
                "mood": "dramatic, emotional, cinematic"
            },
            {
                "name": "fade_out",
                "description": "Smooth fade out to black",
                "use_case": "Closing shots, dramatic moments, emotional scenes",
                "technical": "Opacity transition from 1 to 0 over 1 second",
                "mood": "dramatic, emotional, cinematic"
            },
            {
                "name": "crossfade",
                "description": "Smooth blend between two clips",
                "use_case": "Seamless transitions, related photos, story flow",
                "technical": "Opacity blend between clips over 0.5 seconds",
                "mood": "smooth, seamless, flowing"
            },
            {
                "name": "slide_left",
                "description": "Slide in from right, slide out to left",
                "use_case": "Dynamic transitions, action shots, energetic moments",
                "technical": "Horizontal position transition from right to left",
                "mood": "dynamic, energetic, cinematic"
            },
            {
                "name": "slide_right",
                "description": "Slide in from left, slide out to right",
                "use_case": "Dynamic transitions, action shots, energetic moments",
                "technical": "Horizontal position transition from left to right",
                "mood": "dynamic, energetic, cinematic"
            },
            {
                "name": "zoom_transition",
                "description": "Zoom in/out transition effect",
                "use_case": "Dynamic transitions, action shots, energetic moments",
                "technical": "Scale transition with position change",
                "mood": "dynamic, energetic, cinematic"
            },
            {
                "name": "dissolve",
                "description": "Soft dissolve between clips",
                "use_case": "Gentle transitions, romantic moments, soft scenes",
                "technical": "Opacity blend over 1 second",
                "mood": "gentle, romantic, soft"
            }
        ]
    
    def _get_music_styles(self):
        """Get sample music styles"""
        return [
            {
                "name": "nostalgic",
                "description": "Warm, sentimental music for memories",
                "use_case": "Family photos, childhood memories, sentimental moments",
                "technical": "Slow tempo, warm tones, emotional progression",
                "mood": "warm, sentimental, emotional",
                "instruments": "piano, strings, soft synthesizer",
                "tempo": "slow to moderate",
                "key": "major keys, warm progressions"
            },
            {
                "name": "upbeat",
                "description": "Energetic, positive music for celebrations",
                "use_case": "Party photos, celebrations, happy moments",
                "technical": "Fast tempo, bright tones, energetic rhythm",
                "mood": "energetic, positive, celebratory",
                "instruments": "drums, bass, bright synthesizer",
                "tempo": "fast",
                "key": "major keys, bright progressions"
            },
            {
                "name": "romantic",
                "description": "Soft, romantic music for intimate moments",
                "use_case": "Couple photos, romantic moments, intimate scenes",
                "technical": "Moderate tempo, soft tones, romantic progression",
                "mood": "romantic, intimate, soft",
                "instruments": "piano, strings, soft synthesizer",
                "tempo": "moderate",
                "key": "major keys, romantic progressions"
            },
            {
                "name": "energetic",
                "description": "High-energy music for action and excitement",
                "use_case": "Sports photos, action shots, exciting moments",
                "technical": "Very fast tempo, dynamic tones, energetic rhythm",
                "mood": "energetic, exciting, dynamic",
                "instruments": "drums, bass, electric guitar, synthesizer",
                "tempo": "very fast",
                "key": "major keys, energetic progressions"
            },
            {
                "name": "calm",
                "description": "Peaceful, relaxing music for serene moments",
                "use_case": "Nature photos, peaceful moments, relaxing scenes",
                "technical": "Slow tempo, soft tones, peaceful progression",
                "mood": "calm, peaceful, relaxing",
                "instruments": "piano, strings, soft synthesizer",
                "tempo": "slow",
                "key": "major keys, peaceful progressions"
            },
            {
                "name": "dramatic",
                "description": "Intense, dramatic music for powerful moments",
                "use_case": "Important events, dramatic moments, powerful scenes",
                "technical": "Variable tempo, dynamic tones, dramatic progression",
                "mood": "dramatic, intense, powerful",
                "instruments": "orchestra, strings, piano, synthesizer",
                "tempo": "variable",
                "key": "minor keys, dramatic progressions"
            }
        ]
    
    def _get_video_templates(self):
        """Get sample video templates"""
        return [
            {
                "name": "family_memories",
                "description": "Template for family photo collections",
                "context_keywords": ["family", "children", "parents", "home", "love"],
                "effects": ["ken_burns_zoom_in", "static", "ken_burns_zoom_out"],
                "transitions": ["fade_in", "crossfade", "fade_out"],
                "music_style": "nostalgic",
                "duration_per_photo": 4,
                "mood": "warm, sentimental, emotional"
            },
            {
                "name": "travel_adventure",
                "description": "Template for travel and adventure photos",
                "context_keywords": ["travel", "adventure", "landscape", "nature", "explore"],
                "effects": ["pan_left", "pan_right", "ken_burns_zoom_out"],
                "transitions": ["slide_left", "slide_right", "crossfade"],
                "music_style": "energetic",
                "duration_per_photo": 3,
                "mood": "dynamic, adventurous, exciting"
            },
            {
                "name": "romantic_moments",
                "description": "Template for romantic and couple photos",
                "context_keywords": ["romantic", "couple", "love", "wedding", "intimate"],
                "effects": ["ken_burns_zoom_in", "static", "ken_burns_zoom_in"],
                "transitions": ["fade_in", "dissolve", "fade_out"],
                "music_style": "romantic",
                "duration_per_photo": 5,
                "mood": "romantic, intimate, soft"
            },
            {
                "name": "celebration_party",
                "description": "Template for party and celebration photos",
                "context_keywords": ["party", "celebration", "birthday", "festival", "fun"],
                "effects": ["zoom_in_center", "zoom_out_center", "static"],
                "transitions": ["zoom_transition", "crossfade", "slide_left"],
                "music_style": "upbeat",
                "duration_per_photo": 2,
                "mood": "energetic, fun, celebratory"
            },
            {
                "name": "nature_serene",
                "description": "Template for nature and peaceful photos",
                "context_keywords": ["nature", "landscape", "peaceful", "calm", "serene"],
                "effects": ["ken_burns_zoom_out", "pan_left", "pan_right"],
                "transitions": ["fade_in", "crossfade", "fade_out"],
                "music_style": "calm",
                "duration_per_photo": 4,
                "mood": "peaceful, calm, serene"
            },
            {
                "name": "dramatic_moments",
                "description": "Template for important and dramatic moments",
                "context_keywords": ["important", "dramatic", "significant", "milestone", "achievement"],
                "effects": ["ken_burns_zoom_in", "static", "ken_burns_zoom_out"],
                "transitions": ["fade_in", "crossfade", "fade_out"],
                "music_style": "dramatic",
                "duration_per_photo": 5,
                "mood": "dramatic, important, powerful"
            }
        ]
    
    def get_relevant_effects(self, context: str, photo_count: int) -> List[Dict]:
        """Get relevant video effects based on context - always return varied effects"""
        # Always return varied effects for better video quality
        varied_effects = [
            self.database["video_effects"][0],  # ken_burns_zoom_in
            self.database["video_effects"][2],  # pan_left
            self.database["video_effects"][3],  # pan_right
            self.database["video_effects"][5],  # zoom_in_center
            self.database["video_effects"][6],  # zoom_out_center
            self.database["video_effects"][1],  # ken_burns_zoom_out
            self.database["video_effects"][4]   # static
        ]
        
        # Return enough effects for all photos, cycling through if needed
        if len(varied_effects) < photo_count:
            # Cycle through effects to fill all photos
            while len(varied_effects) < photo_count:
                varied_effects.extend(self.database["video_effects"])
        
        return varied_effects[:photo_count]
    
    def get_relevant_transitions(self, context: str, photo_count: int) -> List[Dict]:
        """Get relevant transitions based on context - always return varied transitions"""
        # Always return varied transitions for better video quality
        varied_transitions = [
            self.database["transitions"][0],  # fade_in
            self.database["transitions"][2],  # crossfade
            self.database["transitions"][3],  # slide_left
            self.database["transitions"][4],  # slide_right
            self.database["transitions"][5],  # zoom_transition
            self.database["transitions"][6],  # dissolve
            self.database["transitions"][1]   # fade_out
        ]
        
        # Return enough transitions for all photos, cycling through if needed
        if len(varied_transitions) < photo_count:
            # Cycle through transitions to fill all photos
            while len(varied_transitions) < photo_count:
                varied_transitions.extend(self.database["transitions"])
        
        return varied_transitions[:photo_count]
    
    def get_relevant_music(self, context: str) -> Dict:
        """Get relevant music style based on context"""
        context_lower = context.lower()
        
        for music in self.database["music_styles"]:
            # Check if music style matches context
            if any(keyword in context_lower for keyword in music["use_case"].lower().split(", ")):
                return music
            elif any(keyword in context_lower for keyword in music["mood"].lower().split(", ")):
                return music
        
        # If no specific match, return nostalgic as default
        return self.database["music_styles"][0]
    
    def get_relevant_template(self, context: str) -> Dict:
        """Get relevant video template based on context"""
        context_lower = context.lower()
        
        for template in self.database["video_templates"]:
            # Check if template matches context
            if any(keyword in context_lower for keyword in template["context_keywords"]):
                return template
        
        # If no specific match, return family_memories as default
        return self.database["video_templates"][0]
    
    def get_rag_context(self, context: str, photo_count: int) -> Dict:
        """Get complete RAG context for video generation"""
        return {
            "context": context,
            "photo_count": photo_count,
            "effects": self.get_relevant_effects(context, photo_count),
            "transitions": self.get_relevant_transitions(context, photo_count),
            "music_style": self.get_relevant_music(context),
            "template": self.get_relevant_template(context)
        }

import os
import google.generativeai as genai
from typing import List, Dict, Any
from services.rag_database import RAGDatabase

class RAGGeminiService:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
            print("Warning: GEMINI_API_KEY not found. Using fallback planning.")
        
        self.rag_db = RAGDatabase()
    
    def plan_video_with_rag(self, photo_paths: List[str], context: str) -> Dict[str, Any]:
        """
        Plan video using RAG database and Gemini AI
        """
        try:
            photo_count = len(photo_paths)
            
            # Get RAG context
            rag_context = self.rag_db.get_rag_context(context, photo_count)
            
            if self.model:
                # Use Gemini with RAG context
                return self._plan_with_gemini_rag(rag_context, photo_count)
            else:
                # Use RAG database directly
                return self._plan_with_rag_only(rag_context, photo_count)
                
        except Exception as e:
            print(f"Error in RAG video planning: {str(e)}")
            return self._get_fallback_plan(photo_count)
    
    def _plan_with_gemini_rag(self, rag_context: Dict, photo_count: int) -> Dict[str, Any]:
        """Plan video using Gemini with RAG context"""
        try:
            # Create prompt with RAG context
            prompt = self._create_rag_prompt(rag_context, photo_count)
            
            # Get response from Gemini
            response = self.model.generate_content(prompt)
            plan_text = response.text
            
            # Parse the response
            return self._parse_gemini_response(plan_text, rag_context, photo_count)
            
        except Exception as e:
            print(f"Error with Gemini RAG planning: {str(e)}")
            return self._plan_with_rag_only(rag_context, photo_count)
    
    def _create_rag_prompt(self, rag_context: Dict, photo_count: int) -> str:
        """Create prompt for Gemini with RAG context"""
        effects = rag_context["effects"]
        transitions = rag_context["transitions"]
        music_style = rag_context["music_style"]
        template = rag_context["template"]
        
        prompt = f"""
You are a professional video editor creating a memory video from photos. Use the provided RAG database context to create a detailed video plan.

CONTEXT: {rag_context["context"]}
PHOTO COUNT: {photo_count}

RAG DATABASE CONTEXT:
- Video Effects Available: {[effect["name"] for effect in effects]}
- Transitions Available: {[transition["name"] for transition in transitions]}
- Music Style: {music_style["name"]} - {music_style["description"]}
- Template: {template["name"]} - {template["description"]}

Create a detailed video plan with:
1. Photo sequence (0 to {photo_count-1})
2. Specific effects for each photo (from available effects)
3. Specific transitions between photos (from available transitions)
4. Music style and volume
5. Duration per photo
6. Overall video style and mood

Format your response as JSON with these exact keys:
- "sequence": [0, 1, 2, ...]
- "effects": ["effect1", "effect2", ...]
- "transitions": ["transition1", "transition2", ...]
- "music_style": "style_name"
- "duration_per_photo": number
- "video_style": "description"
- "mood": "description"

Use only the effects and transitions provided in the RAG database. Be creative but stay within the available options.
"""
        return prompt
    
    def _parse_gemini_response(self, response_text: str, rag_context: Dict, photo_count: int) -> Dict[str, Any]:
        """Parse Gemini response and validate against RAG database"""
        try:
            # Try to extract JSON from response
            import json
            import re
            
            # Look for JSON in the response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                plan = json.loads(json_match.group())
            else:
                # Fallback to RAG-only planning
                return self._plan_with_rag_only(rag_context, photo_count)
            
            # Validate and fix the plan
            return self._validate_and_fix_plan(plan, rag_context, photo_count)
            
        except Exception as e:
            print(f"Error parsing Gemini response: {str(e)}")
            return self._plan_with_rag_only(rag_context, photo_count)
    
    def _validate_and_fix_plan(self, plan: Dict, rag_context: Dict, photo_count: int) -> Dict[str, Any]:
        """Validate plan against RAG database and fix any issues"""
        # Ensure sequence is correct
        if "sequence" not in plan or len(plan["sequence"]) != photo_count:
            plan["sequence"] = list(range(photo_count))
        
        # Validate effects
        available_effects = [effect["name"] for effect in rag_context["effects"]]
        if "effects" not in plan or len(plan["effects"]) != photo_count:
            plan["effects"] = [available_effects[i % len(available_effects)] for i in range(photo_count)]
        else:
            # Fix invalid effects
            for i, effect in enumerate(plan["effects"]):
                if effect not in available_effects:
                    plan["effects"][i] = available_effects[i % len(available_effects)]
        
        # Validate transitions
        available_transitions = [transition["name"] for transition in rag_context["transitions"]]
        if "transitions" not in plan or len(plan["transitions"]) != photo_count:
            plan["transitions"] = [available_transitions[i % len(available_transitions)] for i in range(photo_count)]
        else:
            # Fix invalid transitions
            for i, transition in enumerate(plan["transitions"]):
                if transition not in available_transitions:
                    plan["transitions"][i] = available_transitions[i % len(available_transitions)]
        
        # Validate music style
        if "music_style" not in plan or plan["music_style"] != rag_context["music_style"]["name"]:
            plan["music_style"] = rag_context["music_style"]["name"]
        
        # Set default values
        if "duration_per_photo" not in plan:
            plan["duration_per_photo"] = rag_context["template"]["duration_per_photo"]
        
        if "video_style" not in plan:
            plan["video_style"] = rag_context["template"]["mood"]
        
        if "mood" not in plan:
            plan["mood"] = rag_context["template"]["mood"]
        
        return plan
    
    def _plan_with_rag_only(self, rag_context: Dict, photo_count: int) -> Dict[str, Any]:
        """Plan video using only RAG database (no Gemini)"""
        template = rag_context["template"]
        effects = rag_context["effects"]
        transitions = rag_context["transitions"]
        music_style = rag_context["music_style"]
        
        # Create sequence
        sequence = list(range(photo_count))
        
        # Create varied effects list using RAG database
        effects_list = []
        available_effects = [effect["name"] for effect in effects]
        
        # Always use varied effects from RAG database
        for i in range(photo_count):
            effect_index = i % len(available_effects)
            effects_list.append(available_effects[effect_index])
        
        # Create varied transitions list using RAG database
        transitions_list = []
        available_transitions = [transition["name"] for transition in transitions]
        
        # Always use varied transitions from RAG database
        for i in range(photo_count):
            transition_index = i % len(available_transitions)
            transitions_list.append(available_transitions[transition_index])
        
        return {
            "sequence": sequence,
            "effects": effects_list,
            "transitions": transitions_list,
            "music_style": music_style["name"],
            "duration_per_photo": template["duration_per_photo"],
            "video_style": template["mood"],
            "mood": template["mood"]
        }
    
    def _get_fallback_plan(self, photo_count: int) -> Dict[str, Any]:
        """Get fallback plan when everything fails"""
        return {
            "sequence": list(range(photo_count)),
            "effects": ["static"] * photo_count,
            "transitions": ["fade"] * photo_count,
            "music_style": "nostalgic",
            "duration_per_photo": 3,
            "video_style": "simple and clean",
            "mood": "peaceful"
        }

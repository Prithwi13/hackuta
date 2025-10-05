#!/usr/bin/env python3
"""
Enhanced context generator with CLIP embeddings and better captioning
"""

import os
import numpy as np
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel, BlipProcessor, BlipForConditionalGeneration
import spacy
from typing import List, Dict, Any
import json

class EnhancedContextGenerator:
    def __init__(self):
        """Initialize enhanced context generator with CLIP and BLIP models"""
        print("Loading enhanced context generation models...")
        
        # Load CLIP for semantic embeddings
        self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        
        # Load BLIP for better image captioning
        self.blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        
        # Load spaCy for NER
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Scene classification templates
        self.scene_templates = [
            "a family gathering with people",
            "a romantic couple moment",
            "a travel adventure scene",
            "a party celebration event",
            "a nature landscape view",
            "a dramatic important moment",
            "a peaceful calm scene",
            "a business professional setting"
        ]
        
        print("Enhanced context generation models loaded successfully!")

    def generate_context(self, photo_paths: List[str]) -> Dict[str, Any]:
        """
        Generate enhanced context using CLIP embeddings, BLIP captions, and NER
        """
        try:
            individual_captions = []
            clip_embeddings = []
            scene_classifications = []
            entities = []
            
            for i, photo_path in enumerate(photo_paths):
                print(f"Processing photo {i+1}/{len(photo_paths)}: {os.path.basename(photo_path)}")
                
                # Load and process image
                image = Image.open(photo_path).convert('RGB')
                
                # Generate BLIP caption
                caption = self._generate_blip_caption(image)
                
                # Generate CLIP embedding
                embedding = self._generate_clip_embedding(image)
                
                # Classify scene
                scene = self._classify_scene(image, embedding)
                
                # Extract entities from caption
                photo_entities = self._extract_entities(caption)
                
                individual_captions.append({
                    'caption': caption,
                    'photo': os.path.basename(photo_path),
                    'scene': scene,
                    'entities': photo_entities
                })
                
                clip_embeddings.append(embedding)
                scene_classifications.append(scene)
                entities.extend(photo_entities)
            
            # Generate overall context
            overall_context = self._generate_overall_context(individual_captions, scene_classifications, entities)
            
            # Generate semantic themes
            themes = self._extract_themes(individual_captions, scene_classifications)
            
            return {
                'individual_captions': individual_captions,
                'overall_context': overall_context,
                'photo_count': len(photo_paths),
                'clip_embeddings': clip_embeddings,
                'scene_classifications': scene_classifications,
                'entities': list(set(entities)),
                'themes': themes
            }
            
        except Exception as e:
            print(f"Error in enhanced context generation: {str(e)}")
            return {
                'individual_captions': [],
                'overall_context': 'Unable to generate enhanced context',
                'photo_count': len(photo_paths),
                'clip_embeddings': [],
                'scene_classifications': [],
                'entities': [],
                'themes': []
            }

    def _generate_blip_caption(self, image: Image.Image) -> str:
        """Generate caption using BLIP model"""
        try:
            inputs = self.blip_processor(image, return_tensors="pt")
            out = self.blip_model.generate(**inputs, max_length=50, num_beams=5)
            caption = self.blip_processor.decode(out[0], skip_special_tokens=True)
            return caption
        except Exception as e:
            print(f"Error generating BLIP caption: {str(e)}")
            return "A photo"

    def _generate_clip_embedding(self, image: Image.Image) -> np.ndarray:
        """Generate CLIP embedding for semantic similarity"""
        try:
            inputs = self.clip_processor(images=image, return_tensors="pt")
            with torch.no_grad():
                image_features = self.clip_model.get_image_features(**inputs)
                # Normalize embeddings
                image_features = image_features / image_features.norm(dim=-1, keepdim=True)
                return image_features.numpy().flatten()
        except Exception as e:
            print(f"Error generating CLIP embedding: {str(e)}")
            return np.zeros(512)  # Default embedding size

    def _classify_scene(self, image: Image.Image, embedding: np.ndarray) -> str:
        """Classify scene using CLIP similarity with templates"""
        try:
            # Get text embeddings for scene templates
            text_inputs = self.clip_processor(text=self.scene_templates, return_tensors="pt", padding=True)
            with torch.no_grad():
                text_features = self.clip_model.get_text_features(**text_inputs)
                text_features = text_features / text_features.norm(dim=-1, keepdim=True)
            
            # Calculate similarities
            similarities = torch.cosine_similarity(
                torch.tensor(embedding).unsqueeze(0), 
                text_features
            )
            
            # Get best matching scene
            best_match_idx = similarities.argmax().item()
            return self.scene_templates[best_match_idx]
            
        except Exception as e:
            print(f"Error classifying scene: {str(e)}")
            return "a general photo scene"

    def _extract_entities(self, text: str) -> List[str]:
        """Extract named entities using spaCy"""
        if not self.nlp:
            return []
        
        try:
            doc = self.nlp(text)
            entities = []
            for ent in doc.ents:
                if ent.label_ in ['PERSON', 'ORG', 'GPE', 'EVENT', 'WORK_OF_ART']:
                    entities.append(ent.text.lower())
            return entities
        except Exception as e:
            print(f"Error extracting entities: {str(e)}")
            return []

    def _generate_overall_context(self, captions: List[Dict], scenes: List[str], entities: List[str]) -> str:
        """Generate comprehensive overall context"""
        try:
            # Extract key themes
            all_captions = [c['caption'] for c in captions]
            all_scenes = scenes
            unique_entities = list(set(entities))
            
            # Create context summary
            context_parts = []
            
            if all_captions:
                context_parts.append(f"Photo collection contains: {', '.join(all_captions[:3])}")
            
            if unique_entities:
                context_parts.append(f"Key elements: {', '.join(unique_entities[:5])}")
            
            if all_scenes:
                scene_counts = {}
                for scene in all_scenes:
                    scene_counts[scene] = scene_counts.get(scene, 0) + 1
                dominant_scene = max(scene_counts, key=scene_counts.get)
                context_parts.append(f"Main theme: {dominant_scene}")
            
            return ". ".join(context_parts) + f". Total photos: {len(captions)}"
            
        except Exception as e:
            print(f"Error generating overall context: {str(e)}")
            return "Photo collection with various scenes and elements"

    def _extract_themes(self, captions: List[Dict], scenes: List[str]) -> List[str]:
        """Extract semantic themes from captions and scenes"""
        try:
            themes = []
            
            # Extract themes from scenes
            for scene in scenes:
                if "family" in scene.lower():
                    themes.append("family")
                elif "romantic" in scene.lower():
                    themes.append("romantic")
                elif "travel" in scene.lower():
                    themes.append("travel")
                elif "party" in scene.lower():
                    themes.append("celebration")
                elif "nature" in scene.lower():
                    themes.append("nature")
                elif "dramatic" in scene.lower():
                    themes.append("dramatic")
                elif "peaceful" in scene.lower():
                    themes.append("calm")
                elif "business" in scene.lower():
                    themes.append("professional")
            
            # Extract themes from captions
            for caption in captions:
                text = caption['caption'].lower()
                if any(word in text for word in ['wedding', 'marriage', 'bride', 'groom']):
                    themes.append("wedding")
                elif any(word in text for word in ['birthday', 'party', 'celebration']):
                    themes.append("celebration")
                elif any(word in text for word in ['travel', 'vacation', 'trip', 'journey']):
                    themes.append("travel")
                elif any(word in text for word in ['nature', 'landscape', 'mountain', 'ocean']):
                    themes.append("nature")
                elif any(word in text for word in ['family', 'children', 'kids', 'parents']):
                    themes.append("family")
            
            return list(set(themes))
            
        except Exception as e:
            print(f"Error extracting themes: {str(e)}")
            return []

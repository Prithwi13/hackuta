#!/usr/bin/env python3
"""
Vector-based RAG database with FAISS for semantic retrieval
"""

import os
import json
import numpy as np
import faiss
from typing import List, Dict, Any, Tuple
import pickle
from sentence_transformers import SentenceTransformer

class VectorRAGDatabase:
    def __init__(self, database_path: str = "rag_database.json", embeddings_path: str = "embeddings.pkl"):
        """Initialize vector RAG database with FAISS"""
        self.database_path = database_path
        self.embeddings_path = embeddings_path
        
        # Load sentence transformer for text embeddings
        print("Loading sentence transformer for embeddings...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize FAISS index
        self.dimension = 384  # all-MiniLM-L6-v2 dimension
        self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity
        
        # Load or create database
        self.database = self._load_database()
        self._build_or_load_index()
        
        print(f"Vector RAG database initialized with {self.index.ntotal} items")

    def _load_database(self) -> Dict[str, Any]:
        """Load RAG database from JSON file"""
        if os.path.exists(self.database_path):
            with open(self.database_path, 'r') as f:
                return json.load(f)
        else:
            return self._create_default_database()

    def _create_default_database(self) -> Dict[str, Any]:
        """Create default RAG database with rich metadata"""
        return {
            "video_effects": [
                {
                    "name": "ken_burns_zoom_in",
                    "description": "Slow zoom in effect, creates depth and focus",
                    "use_case": "Portrait photos, close-up shots, emotional moments",
                    "technical": "Gradual scale increase from 1.0 to 1.2 over duration",
                    "mood": "intimate, emotional, focused",
                    "keywords": ["zoom", "intimate", "emotional", "portrait", "close-up", "focus"]
                },
                {
                    "name": "ken_burns_zoom_out",
                    "description": "Slow zoom out effect, reveals more context",
                    "use_case": "Landscape photos, group shots, establishing shots",
                    "technical": "Gradual scale decrease from 1.2 to 1.0 over duration",
                    "mood": "expansive, revealing, contextual",
                    "keywords": ["zoom", "landscape", "group", "context", "revealing", "expansive"]
                },
                {
                    "name": "pan_left",
                    "description": "Horizontal pan from right to left",
                    "use_case": "Wide photos, panoramic shots, travel photos",
                    "technical": "Horizontal movement from right edge to left edge",
                    "mood": "dynamic, cinematic, storytelling",
                    "keywords": ["pan", "horizontal", "wide", "panoramic", "travel", "dynamic", "cinematic"]
                },
                {
                    "name": "pan_right",
                    "description": "Horizontal pan from left to right",
                    "use_case": "Wide photos, panoramic shots, travel photos",
                    "technical": "Horizontal movement from left edge to right edge",
                    "mood": "dynamic, cinematic, storytelling",
                    "keywords": ["pan", "horizontal", "wide", "panoramic", "travel", "dynamic", "cinematic"]
                },
                {
                    "name": "static",
                    "description": "No movement, clean and stable",
                    "use_case": "Portrait photos, detailed shots, important moments",
                    "technical": "No transformation applied",
                    "mood": "stable, focused, important",
                    "keywords": ["static", "stable", "focused", "important", "clean", "detailed"]
                },
                {
                    "name": "zoom_in_center",
                    "description": "Zoom in from center point",
                    "use_case": "Portrait photos, detailed shots, emotional moments",
                    "technical": "Scale increase from center point",
                    "mood": "intimate, emotional, focused",
                    "keywords": ["zoom", "center", "intimate", "emotional", "portrait", "focused"]
                },
                {
                    "name": "zoom_out_center",
                    "description": "Zoom out from center point",
                    "use_case": "Group photos, landscape shots, context revealing",
                    "technical": "Scale decrease from center point",
                    "mood": "expansive, revealing, contextual",
                    "keywords": ["zoom", "center", "group", "landscape", "context", "revealing"]
                }
            ],
            "transitions": [
                {
                    "name": "fade_in",
                    "description": "Smooth fade in from black",
                    "use_case": "Opening shots, dramatic moments, emotional scenes",
                    "technical": "Opacity transition from 0 to 1 over 1 second",
                    "mood": "dramatic, emotional, cinematic",
                    "keywords": ["fade", "opening", "dramatic", "emotional", "cinematic", "smooth"]
                },
                {
                    "name": "fade_out",
                    "description": "Smooth fade out to black",
                    "use_case": "Closing shots, dramatic moments, emotional scenes",
                    "technical": "Opacity transition from 1 to 0 over 1 second",
                    "mood": "dramatic, emotional, cinematic",
                    "keywords": ["fade", "closing", "dramatic", "emotional", "cinematic", "smooth"]
                },
                {
                    "name": "crossfade",
                    "description": "Smooth blend between two clips",
                    "use_case": "Seamless transitions, related photos, story flow",
                    "technical": "Opacity blend between clips over 0.5 seconds",
                    "mood": "smooth, seamless, flowing",
                    "keywords": ["crossfade", "blend", "seamless", "smooth", "flowing", "related"]
                },
                {
                    "name": "slide_left",
                    "description": "Slide in from right, slide out to left",
                    "use_case": "Dynamic transitions, action shots, energetic moments",
                    "technical": "Horizontal position transition from right to left",
                    "mood": "dynamic, energetic, cinematic",
                    "keywords": ["slide", "left", "dynamic", "energetic", "action", "cinematic"]
                },
                {
                    "name": "slide_right",
                    "description": "Slide in from left, slide out to right",
                    "use_case": "Dynamic transitions, action shots, energetic moments",
                    "technical": "Horizontal position transition from left to right",
                    "mood": "dynamic, energetic, cinematic",
                    "keywords": ["slide", "right", "dynamic", "energetic", "action", "cinematic"]
                },
                {
                    "name": "zoom_transition",
                    "description": "Zoom in/out transition effect",
                    "use_case": "Dynamic transitions, action shots, energetic moments",
                    "technical": "Scale transition with position change",
                    "mood": "dynamic, energetic, cinematic",
                    "keywords": ["zoom", "transition", "dynamic", "energetic", "action", "scale"]
                },
                {
                    "name": "dissolve",
                    "description": "Soft dissolve between clips",
                    "use_case": "Gentle transitions, romantic moments, soft scenes",
                    "technical": "Opacity blend over 1 second",
                    "mood": "gentle, romantic, soft",
                    "keywords": ["dissolve", "soft", "gentle", "romantic", "blend", "smooth"]
                }
            ],
            "music_styles": [
                {
                    "name": "nostalgic",
                    "description": "Warm, sentimental music for memories",
                    "use_case": "Family photos, childhood memories, sentimental moments",
                    "technical": "Slow tempo, warm tones, emotional progression",
                    "mood": "warm, sentimental, emotional",
                    "instruments": "piano, strings, soft synthesizer",
                    "tempo": "slow to moderate",
                    "key": "major keys, warm progressions",
                    "keywords": ["nostalgic", "warm", "sentimental", "family", "memories", "emotional", "piano"]
                },
                {
                    "name": "upbeat",
                    "description": "Energetic, positive music for celebrations",
                    "use_case": "Party photos, celebrations, happy moments",
                    "technical": "Fast tempo, bright tones, energetic rhythm",
                    "mood": "energetic, positive, celebratory",
                    "instruments": "drums, bass, bright synthesizer",
                    "tempo": "fast",
                    "key": "major keys, bright progressions",
                    "keywords": ["upbeat", "energetic", "positive", "celebration", "party", "happy", "drums"]
                },
                {
                    "name": "romantic",
                    "description": "Soft, romantic music for intimate moments",
                    "use_case": "Couple photos, romantic moments, intimate scenes",
                    "technical": "Moderate tempo, soft tones, romantic progression",
                    "mood": "romantic, intimate, soft",
                    "instruments": "piano, strings, soft synthesizer",
                    "tempo": "moderate",
                    "key": "major keys, romantic progressions",
                    "keywords": ["romantic", "intimate", "soft", "couple", "love", "piano", "strings"]
                },
                {
                    "name": "energetic",
                    "description": "High-energy music for action and excitement",
                    "use_case": "Sports photos, action shots, exciting moments",
                    "technical": "Very fast tempo, dynamic tones, energetic rhythm",
                    "mood": "energetic, exciting, dynamic",
                    "instruments": "drums, bass, electric guitar, synthesizer",
                    "tempo": "very fast",
                    "key": "major keys, energetic progressions",
                    "keywords": ["energetic", "exciting", "dynamic", "sports", "action", "drums", "guitar"]
                },
                {
                    "name": "calm",
                    "description": "Peaceful, relaxing music for serene moments",
                    "use_case": "Nature photos, peaceful moments, relaxing scenes",
                    "technical": "Slow tempo, soft tones, peaceful progression",
                    "mood": "calm, peaceful, relaxing",
                    "instruments": "piano, strings, soft synthesizer",
                    "tempo": "slow",
                    "key": "major keys, peaceful progressions",
                    "keywords": ["calm", "peaceful", "relaxing", "nature", "serene", "soft", "piano"]
                },
                {
                    "name": "dramatic",
                    "description": "Intense, dramatic music for powerful moments",
                    "use_case": "Important events, dramatic moments, powerful scenes",
                    "technical": "Variable tempo, dynamic tones, dramatic progression",
                    "mood": "dramatic, intense, powerful",
                    "instruments": "orchestra, strings, piano, synthesizer",
                    "tempo": "variable",
                    "key": "minor keys, dramatic progressions",
                    "keywords": ["dramatic", "intense", "powerful", "important", "orchestra", "strings", "intense"]
                }
            ],
            "video_templates": [
                {
                    "name": "family_memories",
                    "description": "Template for family photo collections",
                    "context_keywords": ["family", "children", "parents", "home", "love"],
                    "effects": ["ken_burns_zoom_in", "static", "ken_burns_zoom_out"],
                    "transitions": ["fade_in", "crossfade", "fade_out"],
                    "music_style": "nostalgic",
                    "duration_per_photo": 4,
                    "mood": "warm, sentimental, emotional",
                    "keywords": ["family", "memories", "children", "parents", "home", "love", "warm", "sentimental"]
                },
                {
                    "name": "travel_adventure",
                    "description": "Template for travel and adventure photos",
                    "context_keywords": ["travel", "adventure", "landscape", "nature", "explore"],
                    "effects": ["pan_left", "pan_right", "ken_burns_zoom_out"],
                    "transitions": ["slide_left", "slide_right", "crossfade"],
                    "music_style": "energetic",
                    "duration_per_photo": 3,
                    "mood": "dynamic, adventurous, exciting",
                    "keywords": ["travel", "adventure", "landscape", "nature", "explore", "dynamic", "exciting"]
                },
                {
                    "name": "romantic_moments",
                    "description": "Template for romantic and couple photos",
                    "context_keywords": ["romantic", "couple", "love", "wedding", "intimate"],
                    "effects": ["ken_burns_zoom_in", "static", "ken_burns_zoom_in"],
                    "transitions": ["fade_in", "dissolve", "fade_out"],
                    "music_style": "romantic",
                    "duration_per_photo": 5,
                    "mood": "romantic, intimate, soft",
                    "keywords": ["romantic", "couple", "love", "wedding", "intimate", "soft", "emotional"]
                },
                {
                    "name": "celebration_party",
                    "description": "Template for party and celebration photos",
                    "context_keywords": ["party", "celebration", "birthday", "festival", "fun"],
                    "effects": ["zoom_in_center", "zoom_out_center", "static"],
                    "transitions": ["zoom_transition", "crossfade", "slide_left"],
                    "music_style": "upbeat",
                    "duration_per_photo": 2,
                    "mood": "energetic, fun, celebratory",
                    "keywords": ["party", "celebration", "birthday", "festival", "fun", "energetic", "upbeat"]
                },
                {
                    "name": "nature_serene",
                    "description": "Template for nature and peaceful photos",
                    "context_keywords": ["nature", "landscape", "peaceful", "calm", "serene"],
                    "effects": ["ken_burns_zoom_out", "pan_left", "pan_right"],
                    "transitions": ["fade_in", "crossfade", "fade_out"],
                    "music_style": "calm",
                    "duration_per_photo": 4,
                    "mood": "peaceful, calm, serene",
                    "keywords": ["nature", "landscape", "peaceful", "calm", "serene", "relaxing", "soft"]
                },
                {
                    "name": "dramatic_moments",
                    "description": "Template for important and dramatic moments",
                    "context_keywords": ["important", "dramatic", "significant", "milestone", "achievement"],
                    "effects": ["ken_burns_zoom_in", "static", "ken_burns_zoom_out"],
                    "transitions": ["fade_in", "crossfade", "fade_out"],
                    "music_style": "dramatic",
                    "duration_per_photo": 5,
                    "mood": "dramatic, important, powerful",
                    "keywords": ["important", "dramatic", "significant", "milestone", "achievement", "powerful", "intense"]
                }
            ]
        }

    def _build_or_load_index(self):
        """Build or load FAISS index with embeddings"""
        if os.path.exists(self.embeddings_path):
            print("Loading existing embeddings...")
            self._load_embeddings()
        else:
            print("Building new embeddings index...")
            self._build_embeddings()

    def _build_embeddings(self):
        """Build embeddings for all RAG items"""
        all_items = []
        item_metadata = []
        
        # Process all items from database
        for category, items in self.database.items():
            for item in items:
                # Create searchable text
                searchable_text = f"{item.get('name', '')} {item.get('description', '')} {item.get('use_case', '')} {item.get('mood', '')} {' '.join(item.get('keywords', []))}"
                
                all_items.append(searchable_text)
                item_metadata.append({
                    'category': category,
                    'item': item,
                    'original_text': searchable_text
                })
        
        # Generate embeddings
        print(f"Generating embeddings for {len(all_items)} items...")
        embeddings = self.embedding_model.encode(all_items, convert_to_tensor=True)
        embeddings = embeddings.cpu().numpy()
        
        # Normalize embeddings for cosine similarity
        embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        
        # Add to FAISS index
        self.index.add(embeddings.astype('float32'))
        
        # Save embeddings and metadata
        self._save_embeddings(embeddings, item_metadata)

    def _save_embeddings(self, embeddings: np.ndarray, metadata: List[Dict]):
        """Save embeddings and metadata"""
        with open(self.embeddings_path, 'wb') as f:
            pickle.dump({
                'embeddings': embeddings,
                'metadata': metadata
            }, f)
        print(f"Saved embeddings to {self.embeddings_path}")

    def _load_embeddings(self):
        """Load existing embeddings"""
        with open(self.embeddings_path, 'rb') as f:
            data = pickle.load(f)
            embeddings = data['embeddings']
            self.item_metadata = data['metadata']
        
        # Add to FAISS index
        self.index.add(embeddings.astype('float32'))
        print(f"Loaded {len(embeddings)} embeddings")

    def semantic_search(self, query: str, k: int = 5, category_filter: str = None) -> List[Dict[str, Any]]:
        """Perform semantic search using FAISS"""
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query], convert_to_tensor=True)
            query_embedding = query_embedding.cpu().numpy()
            query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
            
            # Search in FAISS index
            scores, indices = self.index.search(query_embedding.astype('float32'), k)
            
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.item_metadata):
                    metadata = self.item_metadata[idx]
                    
                    # Apply category filter if specified
                    if category_filter and metadata['category'] != category_filter:
                        continue
                    
                    results.append({
                        'item': metadata['item'],
                        'category': metadata['category'],
                        'score': float(score),
                        'original_text': metadata['original_text']
                    })
            
            return results
            
        except Exception as e:
            print(f"Error in semantic search: {str(e)}")
            return []

    def get_relevant_effects(self, context: str, photo_count: int) -> List[Dict]:
        """Get relevant effects using semantic search"""
        results = self.semantic_search(context, k=photo_count, category_filter="video_effects")
        return [r['item'] for r in results]

    def get_relevant_transitions(self, context: str, photo_count: int) -> List[Dict]:
        """Get relevant transitions using semantic search"""
        results = self.semantic_search(context, k=photo_count, category_filter="transitions")
        return [r['item'] for r in results]

    def get_relevant_music(self, context: str) -> Dict:
        """Get relevant music style using semantic search"""
        results = self.semantic_search(context, k=1, category_filter="music_styles")
        if results:
            return results[0]['item']
        else:
            return self.database["music_styles"][0]  # Default fallback

    def get_relevant_template(self, context: str) -> Dict:
        """Get relevant template using semantic search"""
        results = self.semantic_search(context, k=1, category_filter="video_templates")
        if results:
            return results[0]['item']
        else:
            return self.database["video_templates"][0]  # Default fallback

    def get_rag_context(self, context: str, photo_count: int) -> Dict[str, Any]:
        """Get complete RAG context using semantic search"""
        return {
            'context': context,
            'photo_count': photo_count,
            'effects': self.get_relevant_effects(context, photo_count),
            'transitions': self.get_relevant_transitions(context, photo_count),
            'music_style': self.get_relevant_music(context),
            'template': self.get_relevant_template(context)
        }

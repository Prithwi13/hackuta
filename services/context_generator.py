import os
from transformers import pipeline
from PIL import Image
import torch

class ContextGenerator:
    def __init__(self):
        # Initialize BERT-based image captioning model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.image_captioner = pipeline(
            "image-to-text",
            model="nlpconnect/vit-gpt2-image-captioning",
            device=0 if self.device == "cuda" else -1
        )
    
    def generate_context(self, photo_paths):
        """
        Generate descriptive context from all photos using BERT5 and vision models
        """
        try:
            # Generate individual captions for each photo
            individual_captions = []
            for photo_path in photo_paths:
                try:
                    image = Image.open(photo_path)
                    # Fix the parameter issue
                    caption = self.image_captioner(image)
                    individual_captions.append({
                        'photo': os.path.basename(photo_path),
                        'caption': caption[0]['generated_text']
                    })
                except Exception as e:
                    print(f"Error generating caption for {photo_path}: {str(e)}")
                    individual_captions.append({
                        'photo': os.path.basename(photo_path),
                        'caption': 'Unable to generate caption'
                    })
            
            # Generate overall context
            overall_context = self._generate_overall_context(individual_captions)
            
            return {
                'individual_captions': individual_captions,
                'overall_context': overall_context,
                'photo_count': len(photo_paths)
            }
            
        except Exception as e:
            print(f"Error in context generation: {str(e)}")
            return {
                'individual_captions': [],
                'overall_context': 'Unable to generate context',
                'photo_count': len(photo_paths)
            }
    
    def _generate_overall_context(self, individual_captions):
        """
        Generate overall context from individual captions
        """
        # Combine all captions
        all_captions = [cap['caption'] for cap in individual_captions]
        combined_text = " ".join(all_captions)
        
        # Simple context generation (can be enhanced with more sophisticated NLP)
        context_parts = []
        
        # Count common themes
        themes = self._extract_themes(all_captions)
        if themes:
            context_parts.append(f"This collection features {', '.join(themes)}.")
        
        # Add photo count
        context_parts.append(f"The collection contains {len(individual_captions)} photos.")
        
        # Add time-based context if available
        if len(individual_captions) > 1:
            context_parts.append("The photos appear to be from a sequence or event.")
        
        return " ".join(context_parts) if context_parts else "A collection of photos ready for video creation."
    
    def _extract_themes(self, captions):
        """
        Extract common themes from captions
        """
        # Simple keyword extraction (can be enhanced with more sophisticated NLP)
        common_words = {}
        for caption in captions:
            words = caption.lower().split()
            for word in words:
                if len(word) > 3:  # Only consider words longer than 3 characters
                    common_words[word] = common_words.get(word, 0) + 1
        
        # Get most common themes
        themes = [word for word, count in common_words.items() if count > 1]
        return themes[:5]  # Return top 5 themes




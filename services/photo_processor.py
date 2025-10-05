import os
from PIL import Image
import cv2
import numpy as np
from datetime import datetime

class PhotoProcessor:
    def __init__(self):
        self.supported_formats = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
    
    def process_photos(self, photo_paths):
        """
        Process uploaded photos for optimal video generation
        """
        processed_photos = []
        
        for i, photo_path in enumerate(photo_paths):
            try:
                # Load image
                image = Image.open(photo_path)
                
                # Get image metadata
                metadata = self._extract_metadata(image, photo_path)
                
                # Resize if needed (maintain aspect ratio)
                resized_image = self._resize_image(image)
                
                # Save processed image
                processed_path = self._save_processed_image(resized_image, i)
                
                processed_photos.append({
                    'original_path': photo_path,
                    'processed_path': processed_path,
                    'metadata': metadata,
                    'index': i
                })
                
            except Exception as e:
                print(f"Error processing photo {photo_path}: {str(e)}")
                continue
        
        return processed_photos
    
    def _extract_metadata(self, image, photo_path):
        """Extract metadata from image"""
        metadata = {
            'filename': os.path.basename(photo_path),
            'size': image.size,
            'mode': image.mode,
            'format': image.format,
            'created_time': datetime.fromtimestamp(os.path.getctime(photo_path))
        }
        
        # Try to extract EXIF data
        try:
            exif = image._getexif()
            if exif:
                metadata['exif'] = exif
        except:
            pass
        
        return metadata
    
    def _resize_image(self, image, max_width=1920, max_height=1080):
        """Resize image while maintaining aspect ratio"""
        width, height = image.size
        
        # Calculate new dimensions
        ratio = min(max_width/width, max_height/height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        
        # Resize image
        resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Create new image with target dimensions and paste resized image
        new_image = Image.new('RGB', (max_width, max_height), (0, 0, 0))
        paste_x = (max_width - new_width) // 2
        paste_y = (max_height - new_height) // 2
        new_image.paste(resized, (paste_x, paste_y))
        
        return new_image
    
    def _save_processed_image(self, image, index):
        """Save processed image"""
        filename = f"processed_{index:03d}.jpg"
        filepath = os.path.join('uploads', filename)
        image.save(filepath, 'JPEG', quality=85)
        return filepath
    
    def order_photos(self, photo_paths):
        """
        Order photos based on EXIF data and file timestamps
        """
        try:
            # Create list of photos with metadata
            photos_with_metadata = []
            
            for photo_path in photo_paths:
                try:
                    # Get file modification time
                    file_time = os.path.getmtime(photo_path)
                    
                    # Try to get EXIF date
                    exif_date = None
                    try:
                        with Image.open(photo_path) as img:
                            exif = img._getexif()
                            if exif:
                                # Look for DateTime in EXIF
                                for tag, value in exif.items():
                                    if tag == 306:  # DateTime tag
                                        exif_date = value
                                        break
                    except:
                        pass
                    
                    photos_with_metadata.append({
                        'path': photo_path,
                        'file_time': file_time,
                        'exif_date': exif_date,
                        'sort_time': exif_date if exif_date else file_time
                    })
                    
                except Exception as e:
                    print(f"Error processing metadata for {photo_path}: {str(e)}")
                    # Fallback to file time
                    photos_with_metadata.append({
                        'path': photo_path,
                        'file_time': os.path.getmtime(photo_path),
                        'exif_date': None,
                        'sort_time': os.path.getmtime(photo_path)
                    })
            
            # Sort by sort_time (EXIF date preferred, then file time)
            sorted_photos = sorted(photos_with_metadata, key=lambda x: x['sort_time'])
            
            # Return just the paths in chronological order
            return [photo['path'] for photo in sorted_photos]
            
        except Exception as e:
            print(f"Error ordering photos: {str(e)}")
            # Return original order if sorting fails
            return photo_paths




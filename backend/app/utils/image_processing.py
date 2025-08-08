import io
import numpy as np
from PIL import Image
from typing import Tuple, Optional
from app.config import settings

class ImageProcessor:
    """Handles image preprocessing for dog breed classification models."""
    
    def __init__(self):
        self.target_size = settings.IMAGE_SIZE
        
    def validate_image(self, file_content: bytes) -> bool:
        """Validate if the uploaded file is a valid image."""
        try:
            image = Image.open(io.BytesIO(file_content))
            # Check if it's a valid image format
            image.verify()
            return True
        except Exception:
            return False
    
    def preprocess_image(self, file_content: bytes) -> Optional[np.ndarray]:
        """
        Preprocess image for model prediction.
        
        Args:
            file_content: Raw image bytes
            
        Returns:
            Preprocessed image array ready for model input
        """
        try:
            # Open image from bytes
            image = Image.open(io.BytesIO(file_content))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize image to target size
            image = image.resize(self.target_size, Image.Resampling.LANCZOS)
            
            # Convert to numpy array
            img_array = np.array(image, dtype=np.float32)
            
            # Normalize pixel values to [0, 1]
            img_array = img_array / 255.0
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
            
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None
    
    def get_image_info(self, file_content: bytes) -> dict:
        """Get basic information about the uploaded image."""
        try:
            image = Image.open(io.BytesIO(file_content))
            return {
                "format": image.format,
                "mode": image.mode,
                "size": image.size,
                "file_size": len(file_content)
            }
        except Exception as e:
            return {"error": str(e)}

# Global instance
image_processor = ImageProcessor()

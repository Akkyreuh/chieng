import os
import numpy as np
from typing import Dict, List, Optional
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class DummyModel:
    """Dummy model for demonstration purposes."""
    
    def __init__(self, model_name: str):
        self.name = model_name
        np.random.seed(hash(model_name) % 2**32)  # Different seed per model
    
    def predict(self, image_array: np.ndarray, verbose=0) -> np.ndarray:
        """Generate dummy predictions."""
        batch_size = image_array.shape[0]
        num_classes = len(settings.DOG_BREEDS)
        
        # Generate realistic-looking probabilities
        logits = np.random.normal(0, 1, (batch_size, num_classes))
        # Apply softmax to get probabilities
        exp_logits = np.exp(logits - np.max(logits, axis=1, keepdims=True))
        probabilities = exp_logits / np.sum(exp_logits, axis=1, keepdims=True)
        
        return probabilities

class ModelLoader:
    """Handles loading and management of models (demo version)."""
    
    def __init__(self):
        self.models: Dict[str, DummyModel] = {}
        self.models_dir = settings.MODELS_DIR
        self.model_names = settings.MODEL_NAMES
        
    def load_models(self) -> bool:
        """
        Load all available models from the models directory.
        
        Returns:
            bool: True if at least one model was loaded successfully
        """
        loaded_count = 0
        
        # Create models directory if it doesn't exist
        os.makedirs(self.models_dir, exist_ok=True)
        
        for model_name in self.model_names:
            if self._load_single_model(model_name):
                loaded_count += 1
        
        logger.info(f"Loaded {loaded_count}/{len(self.model_names)} models successfully")
        return loaded_count > 0
    
    def _load_single_model(self, model_name: str) -> bool:
        """
        Load a single model by name (demo version).
        
        Args:
            model_name: Name of the model to load
            
        Returns:
            bool: True if model was loaded successfully
        """
        # Create dummy model for demonstration
        logger.info(f"Creating demo model: {model_name}")
        self.models[model_name] = DummyModel(model_name)
        return True
    
    def get_model(self, model_name: str) -> Optional[DummyModel]:
        """Get a specific model by name."""
        return self.models.get(model_name)
    
    def get_all_models(self) -> Dict[str, DummyModel]:
        """Get all loaded models."""
        return self.models
    
    def get_loaded_model_names(self) -> List[str]:
        """Get names of all loaded models."""
        return list(self.models.keys())
    
    def is_model_loaded(self, model_name: str) -> bool:
        """Check if a specific model is loaded."""
        return model_name in self.models

# Global instance
model_loader = ModelLoader()

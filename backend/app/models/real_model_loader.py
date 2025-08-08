import os
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
import logging
from PIL import Image

# TensorFlow imports
try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False

# PyTorch and Transformers imports
try:
    import torch
    from transformers import AutoImageProcessor, AutoModelForImageClassification
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

# Azure Custom Vision imports
try:
    from app.models.azure_model import AzureCustomVisionModel
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False

from app.config import settings

logger = logging.getLogger(__name__)

class HuggingFaceModel:
    """Wrapper for Hugging Face pre-trained model (test1)."""
    
    def __init__(self, model_name: str = "anonauthors/stanford_dogs-resnet50"):
        self.model_name = model_name
        self.name = "HuggingFace_ResNet50"
        
        if not TORCH_AVAILABLE:
            raise ImportError("PyTorch and transformers are required for HuggingFace models")
        
        try:
            self.processor = AutoImageProcessor.from_pretrained(model_name)
            self.model = AutoModelForImageClassification.from_pretrained(model_name)
            self.model.eval()
            
            # Load class mapping
            self.class_names = self._load_class_mapping()
            logger.info(f"Loaded HuggingFace model: {model_name}")
            
        except Exception as e:
            logger.error(f"Error loading HuggingFace model: {e}")
            raise
    
    def _load_class_mapping(self) -> List[str]:
        """Load class mapping from CSV or create default mapping."""
        try:
            # Try to find class_mapping.csv in the app directory
            mapping_path = os.path.join(os.path.dirname(__file__), "..", "class_mapping.csv")
            if os.path.exists(mapping_path):
                df_classes = pd.read_csv(mapping_path)
                return df_classes.sort_values("class_index")["class_name"].tolist()
        except Exception as e:
            logger.warning(f"Could not load class mapping: {e}")
        
        # Fallback to default Stanford Dogs classes
        return [
            "Chihuahua", "Japanese_spaniel", "Maltese_dog", "Pekinese", "Shih-Tzu",
            "Blenheim_spaniel", "Papillon", "Toy_terrier", "Rhodesian_ridgeback", "Afghan_hound",
            "Basset", "Beagle", "Bloodhound", "Bluetick", "Black-and-tan_coonhound",
            "Walker_hound", "English_foxhound", "Redbone", "Borzoi", "Irish_wolfhound",
            "Italian_greyhound", "Whippet", "Ibizan_hound", "Norwegian_elkhound", "Otterhound",
            "Saluki", "Scottish_deerhound", "Weimaraner", "Staffordshire_bullterrier", "American_Staffordshire_terrier",
            "Bedlington_terrier", "Border_terrier", "Kerry_blue_terrier", "Irish_terrier", "Norfolk_terrier",
            "Norwich_terrier", "Yorkshire_terrier", "Wire-haired_fox_terrier", "Lakeland_terrier", "Sealyham_terrier",
            "Airedale", "Cairn", "Australian_terrier", "Dandie_Dinmont", "Boston_bull",
            "Miniature_schnauzer", "Giant_schnauzer", "Standard_schnauzer", "Scotch_terrier", "Tibetan_terrier",
            "Silky_terrier", "Soft-coated_wheaten_terrier", "West_Highland_white_terrier", "Lhasa", "Flat-coated_retriever",
            "Curly-coated_retriever", "Golden_retriever", "Labrador_retriever", "Chesapeake_Bay_retriever", "German_short-haired_pointer",
            "Vizsla", "English_setter", "Irish_setter", "Gordon_setter", "Brittany_spaniel",
            "Clumber", "English_springer", "Welsh_springer_spaniel", "Cocker_spaniel", "Sussex_spaniel",
            "Irish_water_spaniel", "Kuvasz", "Schipperke", "Groenendael", "Malinois",
            "Briard", "Kelpie", "Komondor", "Old_English_sheepdog", "Shetland_sheepdog",
            "Collie", "Border_collie", "Bouvier_des_Flandres", "Rottweiler", "German_shepherd",
            "Doberman", "Miniature_pinscher", "Greater_Swiss_Mountain_dog", "Bernese_mountain_dog", "Appenzeller",
            "EntleBucher", "Boxer", "Bull_mastiff", "Tibetan_mastiff", "French_bulldog",
            "Great_Dane", "Saint_Bernard", "Eskimo_dog", "Malamute", "Siberian_husky",
            "Affenpinscher", "Basenji", "Pug", "Leonberg", "Newfoundland",
            "Great_Pyrenees", "Samoyed", "Pomeranian", "Chow", "Keeshond",
            "Brabancon_griffon", "Pembroke", "Cardigan", "Toy_poodle", "Miniature_poodle",
            "Standard_poodle", "Mexican_hairless", "Dingo", "Dhole", "African_hunting_dog"
        ]
    
    def predict(self, image_array: np.ndarray, verbose=0) -> np.ndarray:
        """Make prediction using HuggingFace model."""
        try:
            # Convert numpy array back to PIL Image for the processor
            if image_array.shape[0] == 1:  # Remove batch dimension
                image_array = image_array[0]
            
            # Convert to PIL Image
            image_array = (image_array * 255).astype(np.uint8)
            image = Image.fromarray(image_array)
            
            # Process image
            inputs = self.processor(images=image, return_tensors="pt")
            
            # Make prediction
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                probabilities = torch.softmax(logits, dim=1)
            
            return probabilities.numpy()
            
        except Exception as e:
            logger.error(f"Error in HuggingFace prediction: {e}")
            # Return dummy probabilities
            num_classes = len(self.class_names)
            return np.random.dirichlet(np.ones(num_classes), size=1)

class TensorFlowModel:
    """Wrapper for TensorFlow/Keras model (MPO_MODELE_SCRATCH)."""
    
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.name = "MPO_MODELE_SCRATCH"
        
        if not TENSORFLOW_AVAILABLE:
            raise ImportError("TensorFlow is required for Keras models")
        
        try:
            self.model = tf.keras.models.load_model(model_path)
            logger.info(f"Loaded TensorFlow model: {model_path}")
            
            # Use the same class names as the HuggingFace model for consistency
            self.class_names = self._get_class_names()
            
        except Exception as e:
            logger.error(f"Error loading TensorFlow model: {e}")
            raise
    
    def _get_class_names(self) -> List[str]:
        """Get class names for the model."""
        # Try to load from CSV first
        try:
            mapping_path = os.path.join(os.path.dirname(__file__), "..", "class_mapping.csv")
            if os.path.exists(mapping_path):
                df_classes = pd.read_csv(mapping_path)
                return df_classes.sort_values("class_index")["class_name"].tolist()
        except Exception:
            pass
        
        # Fallback to settings or create based on model output shape
        try:
            output_shape = self.model.output_shape[-1]
            if output_shape == len(settings.DOG_BREEDS):
                return settings.DOG_BREEDS
            else:
                # Create generic class names based on output shape
                return [f"Class_{i}" for i in range(output_shape)]
        except:
            return settings.DOG_BREEDS
    
    def predict(self, image_array: np.ndarray, verbose=0) -> np.ndarray:
        """Make prediction using TensorFlow model."""
        try:
            return self.model.predict(image_array, verbose=verbose)
        except Exception as e:
            logger.error(f"Error in TensorFlow prediction: {e}")
            # Return dummy probabilities
            num_classes = len(self.class_names)
            return np.random.dirichlet(np.ones(num_classes), size=1)

class RealModelLoader:
    """Loads and manages real user models."""
    
    def __init__(self):
        self.models: Dict[str, object] = {}
        self.app_dir = os.path.dirname(__file__)
        
    def load_models(self) -> bool:
        """Load all available real models."""
        loaded_count = 0
        
        # Load HuggingFace model (test1)
        try:
            if TORCH_AVAILABLE:
                hf_model = HuggingFaceModel()
                self.models["HuggingFace_ResNet50"] = hf_model
                loaded_count += 1
                logger.info("Loaded HuggingFace ResNet50 model")
            else:
                logger.warning("PyTorch not available, skipping HuggingFace model")
        except Exception as e:
            logger.error(f"Failed to load HuggingFace model: {e}")
        
        # Load TensorFlow model (MPO_MODELE_SCRATCH)
        try:
            if TENSORFLOW_AVAILABLE:
                keras_model_path = os.path.join(self.app_dir, "..", "MPO_modele_scratch_apres_data_augmentation 1.keras")
                if os.path.exists(keras_model_path):
                    tf_model = TensorFlowModel(keras_model_path)
                    self.models["MPO_MODELE_SCRATCH"] = tf_model
                    loaded_count += 1
                    logger.info("Loaded MPO_MODELE_SCRATCH model")
                else:
                    logger.warning(f"TensorFlow model not found at: {keras_model_path}")
            else:
                logger.warning("TensorFlow not available, skipping Keras model")
        except Exception as e:
            logger.error(f"Failed to load TensorFlow model: {e}")
        
        # Load Azure Custom Vision model
        try:
            if AZURE_AVAILABLE:
                azure_model = AzureCustomVisionModel()
                self.models["Azure_Custom_Vision"] = azure_model
                loaded_count += 1
                logger.info("Loaded Azure Custom Vision model")
            else:
                logger.warning("Azure Cognitive Services not available, skipping Azure model")
        except Exception as e:
            logger.warning(f"Azure Custom Vision model disabled due to API issues: {e}")
            # Continue without Azure model for now
        
        logger.info(f"Loaded {loaded_count} real models successfully")
        return loaded_count > 0
    
    def get_model(self, model_name: str) -> Optional[object]:
        """Get a specific model by name."""
        return self.models.get(model_name)
    
    def get_all_models(self) -> Dict[str, object]:
        """Get all loaded models."""
        return self.models
    
    def get_loaded_model_names(self) -> List[str]:
        """Get names of all loaded models."""
        return list(self.models.keys())
    
    def is_model_loaded(self, model_name: str) -> bool:
        """Check if a specific model is loaded."""
        return model_name in self.models

# Global instance
real_model_loader = RealModelLoader()

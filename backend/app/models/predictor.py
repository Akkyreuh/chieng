import numpy as np
from typing import List, Dict, Tuple
import logging

try:
    from app.models.real_model_loader import real_model_loader
    USE_REAL_MODELS = True
except ImportError:
    from app.models.model_loader import model_loader
    USE_REAL_MODELS = False

from app.config import settings

logger = logging.getLogger(__name__)

class DogBreedPredictor:
    
    def __init__(self):
        self.use_real_models = USE_REAL_MODELS
        if self.use_real_models:
            self.model_loader = real_model_loader
        else:
            self.model_loader = model_loader
            
    def predict_single_model(self, image_array: np.ndarray, model_name: str, original_image_bytes: bytes = None) -> List[Dict]:
        """
        Predict dog breed using a single model.
        
        Args:
            image_array: Preprocessed image array
            model_name: Name of the model to use
            
        Returns:
            List of top 3 predictions with breed names and confidence scores
        """
        model = self.model_loader.get_model(model_name)
        if model is None:
            logger.error(f"Model {model_name} not found")
            return []
        
        try:
            # Handle Azure Custom Vision model differently
            if model_name == "Azure_Custom_Vision":
                logger.info(f"Entering Azure Custom Vision prediction section")
                # Azure model needs original image bytes, not numpy array
                if original_image_bytes is None:
                    logger.error("Azure model requires original image bytes")
                    return []
                
                logger.info(f"Azure model has original_image_bytes, calling predict...")
                
                # Azure model returns list of (breed_name, confidence) tuples
                predictions = model.predict(original_image_bytes, verbose=0)
                
                # Format results for Azure model
                results = []
                for breed_name, confidence in predictions:
                    results.append({
                        "breed": breed_name,
                        "confidence": confidence,
                        "percentage": round(confidence * 100, 2)
                    })
                
                return results
            
            else:
                # Standard model prediction (HuggingFace and TensorFlow)
                predictions = model.predict(image_array, verbose=0)
                
                # Get class names from the model if available
                if hasattr(model, 'class_names'):
                    class_names = model.class_names
                else:
                    class_names = settings.DOG_BREEDS
                
                # Get top 3 predictions
                top_indices = np.argsort(predictions[0])[-3:][::-1]
                
                results = []
                for idx in top_indices:
                    if idx < len(class_names):
                        breed_name = class_names[idx]
                    else:
                        breed_name = f"Unknown_Class_{idx}"
                        
                    confidence = float(predictions[0][idx])
                    
                    results.append({
                        "breed": breed_name,
                        "confidence": confidence,
                        "percentage": round(confidence * 100, 2)
                    })
                
                return results
            
        except Exception as e:
            logger.error(f"Error predicting with model {model_name}: {e}")
            return []
    
    def predict_all_models(self, file_content: bytes) -> Dict:
        """
        Predict dog breed using all available models.
        
        Args:
            file_content: Raw image bytes
            
        Returns:
            Dictionary containing predictions from all models and aggregated results
        """
        # Preprocess image
        try:
            from PIL import Image
            import io
            
            # Open and preprocess image
            image = Image.open(io.BytesIO(file_content))
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize to 224x224 (standard for most models)
            image = image.resize((224, 224))
            
            # Convert to numpy array and normalize
            image_array = np.array(image).astype(np.float32) / 255.0
            image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
            
            # Get image info
            image_info = {
                "size": image.size,
                "format": "RGB",
                "dimensions": f"{image.size[0]}x{image.size[1]}"
            }
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            return {"error": "Failed to preprocess image"}
        
        # Get predictions from all models
        model_predictions = {}
        all_predictions = []
        
        loaded_models = self.model_loader.get_loaded_model_names()
        logger.info(f"Using models: {loaded_models}")
        
        for model_name in loaded_models:
            logger.info(f"Processing model: {model_name}")
            # Handle different image preprocessing for different models
            model_image_array = image_array
            
            # MPO_MODELE_SCRATCH expects 150x150 images
            if model_name == "MPO_MODELE_SCRATCH":
                try:
                    from PIL import Image
                    import io
                    
                    # Resize to 150x150 for MPO model
                    original_image = Image.open(io.BytesIO(file_content))
                    if original_image.mode != 'RGB':
                        original_image = original_image.convert('RGB')
                    
                    resized_image = original_image.resize((150, 150))
                    model_image_array = np.array(resized_image).astype(np.float32) / 255.0
                    model_image_array = np.expand_dims(model_image_array, axis=0)
                    
                except Exception as e:
                    logger.error(f"Error resizing image for MPO model: {e}")
                    continue
            
            # Get predictions
            predictions = self.predict_single_model(model_image_array, model_name, file_content)
            if predictions:
                model_predictions[model_name] = predictions
                all_predictions.extend(predictions)
        
        # Aggregate predictions (ensemble method)
        aggregated_results = self._aggregate_predictions(all_predictions)
        
        return {
            "success": True,
            "image_info": image_info,
            "model_predictions": model_predictions,
            "aggregated_results": aggregated_results,
            "models_used": list(model_predictions.keys()),
            "model_types": self._get_model_types()
        }
    
    def _get_model_types(self) -> Dict[str, str]:
        """Get information about model types."""
        model_types = {}
        for model_name in self.model_loader.get_loaded_model_names():
            model = self.model_loader.get_model(model_name)
            if hasattr(model, 'name'):
                if 'HuggingFace' in model.name:
                    model_types[model_name] = "Modèle Pré-entraîné (HuggingFace ResNet50)"
                elif 'MPO_MODELE_SCRATCH' in model.name:
                    model_types[model_name] = "Modèle From Scratch (MPO)"
                else:
                    model_types[model_name] = "Modèle Personnalisé"
            else:
                model_types[model_name] = "Modèle de Démonstration"
        return model_types
    
    def _aggregate_predictions(self, all_predictions: List[Dict]) -> List[Dict]:
        """
        Aggregate predictions from multiple models using weighted average.
        
        Args:
            all_predictions: List of all predictions from all models
            
        Returns:
            Top 3 aggregated predictions
        """
        if not all_predictions:
            return []
        
        # Group predictions by breed
        breed_scores = {}
        for pred in all_predictions:
            breed = pred["breed"]
            confidence = pred["confidence"]
            
            if breed in breed_scores:
                breed_scores[breed].append(confidence)
            else:
                breed_scores[breed] = [confidence]
        
        # Calculate average confidence for each breed
        breed_averages = {}
        for breed, scores in breed_scores.items():
            avg_score = np.mean(scores)
            breed_averages[breed] = avg_score
        
        # Sort by average confidence and get top 3
        sorted_breeds = sorted(breed_averages.items(), key=lambda x: x[1], reverse=True)[:3]
        
        results = []
        for breed, avg_confidence in sorted_breeds:
            results.append({
                "breed": breed,
                "confidence": float(avg_confidence),
                "percentage": round(avg_confidence * 100, 2),
                "model_count": len(breed_scores[breed])
            })
        
        return results

# Global instance
dog_breed_predictor = DogBreedPredictor()

"""
Azure Custom Vision Model for Dog Breed Classification
Extracted from Dog_breed_Azur.ipynb notebook
"""

import logging
from typing import List, Tuple
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

logger = logging.getLogger(__name__)

class AzureCustomVisionModel:
    
    def __init__(self):
        self.project_id = ''
        self.cv_key = ''
        self.cv_endpoint = ''
        self.model_name = 'Iteration1'
        self.name = "Azure_Custom_Vision"
        
        try:
            credentials = ApiKeyCredentials(in_headers={"Prediction-key": self.cv_key})
            self.client = CustomVisionPredictionClient(endpoint=self.cv_endpoint, credentials=credentials)
            logger.info(f"Azure Custom Vision client initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing Azure Custom Vision client: {e}")
            raise
    
    def predict(self, image_bytes: bytes, verbose=0) -> List[Tuple[str, float]]:
        try:
            logger.info(f"Azure model predict called with image_bytes type: {type(image_bytes)}, size: {len(image_bytes) if image_bytes else 'None'}")
            
            logger.info(f"Calling Azure API with project_id: {self.project_id}, model_name: {self.model_name}")
            classification = self.client.classify_image(
                self.project_id, 
                self.model_name, 
                image_bytes
            )
            logger.info(f"Azure API call successful, got {len(classification.predictions)} predictions")
            
            predictions = []
            for prediction in classification.predictions:
                breed_name = prediction.tag_name
                confidence = prediction.probability
                predictions.append((breed_name, confidence))
            
            predictions.sort(key=lambda x: x[1], reverse=True)
            return predictions[:3]
            
        except Exception as e:
            logger.error(f"Error during Azure Custom Vision prediction: {e}")
            return []

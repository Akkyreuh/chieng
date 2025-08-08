from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
import logging
from app.models.predictor import dog_breed_predictor
from app.config import settings

try:
    from app.models.real_model_loader import real_model_loader
    USE_REAL_MODELS = True
except ImportError:
    from app.models.model_loader import model_loader
    USE_REAL_MODELS = False

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/predict")
async def predict_dog_breed(file: UploadFile = File(...)) -> Dict[str, Any]:
    try:
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="File must be an image (JPEG, PNG, WebP)"
            )
        
        file_content = await file.read()
        
        if len(file_content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size too large. Maximum size: {settings.MAX_FILE_SIZE // (1024*1024)}MB"
            )
        
        try:
            from PIL import Image
            import io
            Image.open(io.BytesIO(file_content))
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Invalid image file"
            )
        
        results = dog_breed_predictor.predict_all_models(file_content)
        
        if "error" in results:
            raise HTTPException(
                status_code=500,
                detail=results["error"]
            )
        
        return JSONResponse(content=results)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in predict endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during prediction"
        )

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "service": "Dog Breed Classifier API",
        "version": settings.VERSION
    }

@router.get("/models")
async def get_models_info() -> Dict[str, Any]:
    if USE_REAL_MODELS:
        loaded_models = real_model_loader.get_loaded_model_names()
    else:
        loaded_models = model_loader.get_loaded_model_names()
    
    return {
        "loaded_models": loaded_models,
        "total_models": len(loaded_models),
        "supported_breeds": len(settings.DOG_BREEDS),
        "image_size": settings.IMAGE_SIZE,
        "max_file_size_mb": settings.MAX_FILE_SIZE // (1024 * 1024)
    }

@router.get("/breeds")
async def get_supported_breeds() -> Dict[str, Any]:
    return {
        "breeds": settings.DOG_BREEDS,
        "total_count": len(settings.DOG_BREEDS)
    }

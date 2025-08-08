from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.config import settings
import logging

try:
    from app.models.real_model_loader import real_model_loader
    USE_REAL_MODELS = True
except ImportError:
    USE_REAL_MODELS = False

from app.models.model_loader import model_loader

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    if USE_REAL_MODELS:
        logger.info("Starting Dog Breed Classifier API with REAL MODELS...")
    else:
        logger.info("Starting Dog Breed Classifier API with DEMO MODELS...")
    
    if USE_REAL_MODELS:
        success = real_model_loader.load_models()
        if success:
            loaded_models = real_model_loader.get_loaded_model_names()
            logger.info(f"Real models loaded successfully: {loaded_models}")
            logger.info("Using your real trained models!")
        else:
            logger.warning("Failed to load real models - falling back to demo models")
            model_loader.load_models()
            logger.info("Using demo models - check dependencies for real models")
    else:
        model_loader.load_models()
        logger.info("Using demo models - install dependencies for real models")
    
    yield
    
    logger.info("Shutting down Dog Breed Classifier API...")

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API pour la classification de races de chiens utilisant plusieurs modèles de Deep Learning (HuggingFace + MPO From Scratch)",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    model_info = "Real Models" if USE_REAL_MODELS else "Demo Models"
    return {
        "message": "Dog Breed Classifier API",
        "version": settings.VERSION,
        "model_status": model_info,
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

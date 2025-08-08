export interface BreedPrediction {
  breed: string;
  confidence: number;
  percentage: number;
  model_count?: number;
}

export interface ModelPrediction {
  [modelName: string]: BreedPrediction[];
}

export interface ImageInfo {
  format: string;
  mode: string;
  size: [number, number];
  file_size: number;
}

export interface PredictionResponse {
  success: boolean;
  image_info: ImageInfo;
  model_predictions: ModelPrediction;
  aggregated_results: BreedPrediction[];
  models_used: string[];
}

export interface ApiError {
  detail: string;
}

export interface UploadedImage {
  file: File;
  preview: string;
}

export interface ModelInfo {
  loaded_models: string[];
  total_models: number;
  supported_breeds: number;
  image_size: [number, number];
  max_file_size_mb: number;
}

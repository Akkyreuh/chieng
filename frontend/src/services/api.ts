import axios from 'axios';
import { PredictionResponse, ModelInfo, ApiError } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout for image processing
});

export const apiService = {
  /**
   * Upload image and get breed predictions
   */
  async predictBreed(file: File): Promise<PredictionResponse> {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.post<PredictionResponse>('/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        const apiError = error.response.data as ApiError;
        throw new Error(apiError.detail || 'Erreur lors de la prédiction');
      }
      throw new Error('Erreur de connexion au serveur');
    }
  },

  /**
   * Get API health status
   */
  async getHealth(): Promise<{ status: string; service: string; version: string }> {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      throw new Error('Service indisponible');
    }
  },

  /**
   * Get models information
   */
  async getModelsInfo(): Promise<ModelInfo> {
    try {
      const response = await api.get<ModelInfo>('/models');
      return response.data;
    } catch (error) {
      throw new Error('Impossible de récupérer les informations des modèles');
    }
  },

  /**
   * Get supported breeds list
   */
  async getSupportedBreeds(): Promise<{ breeds: string[]; total_count: number }> {
    try {
      const response = await api.get('/breeds');
      return response.data;
    } catch (error) {
      throw new Error('Impossible de récupérer la liste des races');
    }
  },
};

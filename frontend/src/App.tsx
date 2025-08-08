import React, { useState, useEffect } from 'react';
import { Heart, AlertCircle } from 'lucide-react';
import ImageUploader from './components/ImageUploader';
import ResultsDisplay from './components/ResultsDisplay';
import ModelComparison from './components/ModelComparison';
import { apiService } from './services/api';
import { UploadedImage, PredictionResponse, ModelInfo } from './types';
import './styles/main.css';

const App: React.FC = () => {
  const [uploadedImage, setUploadedImage] = useState<UploadedImage | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<PredictionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [modelInfo, setModelInfo] = useState<ModelInfo | null>(null);

  // Load model info on component mount
  useEffect(() => {
    const loadModelInfo = async () => {
      try {
        const info = await apiService.getModelsInfo();
        setModelInfo(info);
      } catch (err) {
        console.warn('Could not load model info:', err);
      }
    };

    loadModelInfo();
  }, []);

  const handleImageUpload = async (image: UploadedImage) => {
    setUploadedImage(image);
    setError(null);
    setResults(null);
    setIsLoading(true);

    try {
      const predictionResults = await apiService.predictBreed(image.file);
      setResults(predictionResults);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Une erreur est survenue');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    if (uploadedImage) {
      URL.revokeObjectURL(uploadedImage.preview);
    }
    setUploadedImage(null);
    setResults(null);
    setError(null);
  };

  return (
    <div className="app">
      <div className="container">
        {/* Header */}
        <header className="header">
          <h1>🐕 Classificateur de Races de Chiens</h1>
          <p>Découvrez la race de votre chien grâce à l'intelligence artificielle</p>
          {modelInfo && (
            <p style={{ fontSize: '1rem', marginTop: '10px', opacity: 0.8 }}>
              {modelInfo.total_models} modèles • {modelInfo.supported_breeds} races supportées
            </p>
          )}
        </header>

        {/* Upload Section */}
        <ImageUploader 
          onImageUpload={handleImageUpload}
          isLoading={isLoading}
        />

        {/* Loading State */}
        {isLoading && (
          <div className="loading">
            <div className="spinner"></div>
            <h3>Analyse en cours...</h3>
            <p>Nos modèles d'IA analysent votre image</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="error">
            <AlertCircle size={20} style={{ marginRight: '10px' }} />
            <strong>Erreur:</strong> {error}
            <button 
              onClick={handleReset}
              className="btn"
              style={{ marginLeft: '15px' }}
            >
              Réessayer
            </button>
          </div>
        )}

        {/* Results */}
        {results && !isLoading && (
          <>
            <ResultsDisplay results={results} />
            
            {/* Detailed Model Comparison */}
            <div style={{ 
              background: 'white', 
              borderRadius: '20px', 
              padding: '40px', 
              boxShadow: '0 20px 40px rgba(0,0,0,0.1)',
              marginBottom: '30px'
            }}>
              <ModelComparison 
                modelPredictions={results.model_predictions}
                aggregatedResults={results.aggregated_results}
              />
            </div>

            {/* Reset Button */}
            <div style={{ textAlign: 'center', marginBottom: '40px' }}>
              <button 
                onClick={handleReset}
                className="btn"
                style={{ fontSize: '1.1rem', padding: '15px 30px' }}
              >
                <Heart size={20} />
                Analyser une nouvelle image
              </button>
            </div>
          </>
        )}

        {/* Footer */}
        <footer style={{ 
          textAlign: 'center', 
          padding: '40px 20px', 
          color: 'white', 
          opacity: 0.8 
        }}>
          <p>
            Développé avec ❤️ • Utilise TensorFlow et React
          </p>
          <p style={{ fontSize: '0.9rem', marginTop: '10px' }}>
            Classification basée sur {modelInfo?.total_models || 3} modèles de Deep Learning
          </p>
        </footer>
      </div>
    </div>
  );
};

export default App;

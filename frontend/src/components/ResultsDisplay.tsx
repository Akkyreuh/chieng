import React from 'react';
import { Trophy, Award, Medal } from 'lucide-react';
import { PredictionResponse } from '../types';

interface ResultsDisplayProps {
  results: PredictionResponse;
}

const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ results }) => {
  const getRankIcon = (rank: number) => {
    switch (rank) {
      case 1:
        return <Trophy size={24} />;
      case 2:
        return <Award size={24} />;
      case 3:
        return <Medal size={24} />;
      default:
        return null;
    }
  };

  const getRankColor = (rank: number) => {
    switch (rank) {
      case 1:
        return 'linear-gradient(135deg, #FFD700 0%, #FFA500 100%)'; // Gold
      case 2:
        return 'linear-gradient(135deg, #C0C0C0 0%, #A0A0A0 100%)'; // Silver
      case 3:
        return 'linear-gradient(135deg, #CD7F32 0%, #B8860B 100%)'; // Bronze
      default:
        return 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
    }
  };

  return (
    <div className="results-section">
      <div className="results-header">
        <h2>Résultats de la Classification</h2>
        <p>Analyse réalisée par {results.models_used.length} modèle(s) de Deep Learning</p>
      </div>

      {/* Aggregated Results */}
      <div className="aggregated-results">
        <h3>🏆 Top 3 des Races (Résultats Agrégés)</h3>
        <div className="top-predictions">
          {results.aggregated_results.slice(0, 3).map((prediction, index) => (
            <div 
              key={prediction.breed}
              className="prediction-card"
              style={{ background: getRankColor(index + 1) }}
            >
              <div className="prediction-rank">#{index + 1}</div>
              <div className="prediction-breed">
                {getRankIcon(index + 1)}
                <div style={{ marginTop: '10px' }}>{prediction.breed}</div>
              </div>
              <div className="prediction-confidence">
                {prediction.percentage}%
              </div>
              <div className="confidence-bar">
                <div 
                  className="confidence-fill"
                  style={{ width: `${prediction.percentage}%` }}
                />
              </div>
              {prediction.model_count && (
                <p style={{ fontSize: '0.9rem', marginTop: '10px', opacity: 0.9 }}>
                  Confirmé par {prediction.model_count} modèle(s)
                </p>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Model Comparison */}
      <div className="model-comparison">
        <h3>📊 Comparaison des Modèles</h3>
        <div className="models-grid">
          {Object.entries(results.model_predictions).map(([modelName, predictions]) => (
            <div key={modelName} className="model-card">
              <div className="model-header">
                <div className="model-name">{modelName.toUpperCase()}</div>
                <p style={{ fontSize: '0.9rem', color: '#666' }}>
                  Top 3 des prédictions
                </p>
              </div>
              <div className="model-predictions">
                {predictions.slice(0, 3).map((prediction, index) => (
                  <div key={`${modelName}-${prediction.breed}`} className="model-prediction">
                    <span className="breed-name">
                      #{index + 1} {prediction.breed}
                    </span>
                    <span className="confidence-score">
                      {prediction.percentage}%
                    </span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Image Information */}
      {results.image_info && (
        <div style={{ marginTop: '30px', padding: '20px', background: '#f8f9ff', borderRadius: '15px' }}>
          <h4 style={{ color: '#667eea', marginBottom: '15px' }}>ℹ️ Informations sur l'image</h4>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px', fontSize: '0.9rem' }}>
            <div>
              <strong>Format:</strong> {results.image_info.format}
            </div>
            <div>
              <strong>Mode:</strong> {results.image_info.mode}
            </div>
            <div>
              <strong>Dimensions:</strong> {results.image_info.size[0]} × {results.image_info.size[1]}px
            </div>
            <div>
              <strong>Taille:</strong> {(results.image_info.file_size / 1024 / 1024).toFixed(2)} MB
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultsDisplay;

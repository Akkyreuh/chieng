import React from 'react';
import { BarChart3, Brain, Zap } from 'lucide-react';
import { ModelPrediction, BreedPrediction } from '../types';

interface ModelComparisonProps {
  modelPredictions: ModelPrediction;
  aggregatedResults: BreedPrediction[];
}

const ModelComparison: React.FC<ModelComparisonProps> = ({ 
  modelPredictions, 
  aggregatedResults 
}) => {
  const modelNames = Object.keys(modelPredictions);
  
  // Get consensus breeds (breeds that appear in multiple models' top predictions)
  const getConsensusBreeds = () => {
    const breedCounts: { [breed: string]: number } = {};
    
    Object.values(modelPredictions).forEach(predictions => {
      predictions.slice(0, 3).forEach(pred => {
        breedCounts[pred.breed] = (breedCounts[pred.breed] || 0) + 1;
      });
    });
    
    return Object.entries(breedCounts)
      .filter(([_, count]) => count > 1)
      .sort(([_, a], [__, b]) => b - a)
      .map(([breed, count]) => ({ breed, count }));
  };

  const consensusBreeds = getConsensusBreeds();

  const getModelIcon = (modelName: string) => {
    const icons = [Brain, Zap, BarChart3];
    const index = modelNames.indexOf(modelName);
    const IconComponent = icons[index % icons.length];
    return <IconComponent size={20} />;
  };

  const getAgreementLevel = () => {
    if (consensusBreeds.length === 0) return { level: 'Faible', color: '#ff6b6b', percentage: 0 };
    
    const topBreed = aggregatedResults[0]?.breed;
    const modelsAgreeingOnTop = Object.values(modelPredictions).filter(
      predictions => predictions[0]?.breed === topBreed
    ).length;
    
    const agreementPercentage = (modelsAgreeingOnTop / modelNames.length) * 100;
    
    if (agreementPercentage >= 66) return { level: 'Élevé', color: '#51cf66', percentage: agreementPercentage };
    if (agreementPercentage >= 33) return { level: 'Modéré', color: '#ffd43b', percentage: agreementPercentage };
    return { level: 'Faible', color: '#ff6b6b', percentage: agreementPercentage };
  };

  const agreement = getAgreementLevel();

  return (
    <div className="model-comparison-detailed">
      {/* Agreement Analysis */}
      <div style={{ 
        background: 'white', 
        borderRadius: '15px', 
        padding: '25px', 
        marginBottom: '25px',
        border: `2px solid ${agreement.color}20`
      }}>
        <h3 style={{ color: '#333', marginBottom: '20px', textAlign: 'center' }}>
          🤝 Analyse de Consensus
        </h3>
        
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
          gap: '20px',
          alignItems: 'center'
        }}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ 
              fontSize: '2rem', 
              fontWeight: 'bold', 
              color: agreement.color,
              marginBottom: '10px'
            }}>
              {agreement.percentage.toFixed(0)}%
            </div>
            <div style={{ color: '#666' }}>
              Accord entre modèles
            </div>
            <div style={{ 
              marginTop: '10px',
              padding: '8px 16px',
              background: agreement.color,
              color: 'white',
              borderRadius: '20px',
              display: 'inline-block',
              fontSize: '0.9rem'
            }}>
              Consensus {agreement.level}
            </div>
          </div>
          
          {consensusBreeds.length > 0 && (
            <div>
              <h4 style={{ color: '#667eea', marginBottom: '15px' }}>
                Races en consensus:
              </h4>
              {consensusBreeds.slice(0, 3).map(({ breed, count }) => (
                <div key={breed} style={{ 
                  display: 'flex', 
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '8px 15px',
                  background: '#f8f9ff',
                  borderRadius: '8px',
                  marginBottom: '8px'
                }}>
                  <span style={{ fontWeight: '500' }}>{breed}</span>
                  <span style={{ 
                    background: '#667eea', 
                    color: 'white', 
                    padding: '4px 8px', 
                    borderRadius: '12px',
                    fontSize: '0.8rem'
                  }}>
                    {count}/{modelNames.length}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Individual Model Performance */}
      <div style={{ 
        background: 'white', 
        borderRadius: '15px', 
        padding: '25px'
      }}>
        <h3 style={{ color: '#333', marginBottom: '20px', textAlign: 'center' }}>
          🔬 Performance Individuelle des Modèles
        </h3>
        
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', 
          gap: '20px'
        }}>
          {Object.entries(modelPredictions).map(([modelName, predictions]) => {
            const topPrediction = predictions[0];
            const confidence = topPrediction?.confidence || 0;
            
            return (
              <div key={modelName} style={{
                background: '#f8f9ff',
                border: '2px solid #e0e6ff',
                borderRadius: '12px',
                padding: '20px',
                position: 'relative'
              }}>
                <div style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '10px',
                  marginBottom: '15px'
                }}>
                  <div style={{ color: '#667eea' }}>
                    {getModelIcon(modelName)}
                  </div>
                  <h4 style={{ color: '#667eea', margin: 0 }}>
                    {modelName.toUpperCase()}
                  </h4>
                </div>
                
                {/* Confidence meter */}
                <div style={{ marginBottom: '15px' }}>
                  <div style={{ 
                    display: 'flex', 
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    marginBottom: '8px'
                  }}>
                    <span style={{ fontSize: '0.9rem', color: '#666' }}>
                      Confiance maximale
                    </span>
                    <span style={{ 
                      fontWeight: 'bold', 
                      color: confidence > 0.7 ? '#51cf66' : confidence > 0.4 ? '#ffd43b' : '#ff6b6b'
                    }}>
                      {(confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div style={{ 
                    width: '100%', 
                    height: '8px', 
                    background: '#e0e6ff', 
                    borderRadius: '4px',
                    overflow: 'hidden'
                  }}>
                    <div style={{
                      width: `${confidence * 100}%`,
                      height: '100%',
                      background: confidence > 0.7 ? '#51cf66' : confidence > 0.4 ? '#ffd43b' : '#ff6b6b',
                      borderRadius: '4px',
                      transition: 'width 0.5s ease'
                    }} />
                  </div>
                </div>
                
                {/* Top prediction */}
                <div style={{ 
                  background: 'white',
                  padding: '15px',
                  borderRadius: '8px',
                  border: '1px solid #e0e6ff'
                }}>
                  <div style={{ fontWeight: 'bold', color: '#333', marginBottom: '5px' }}>
                    Prédiction principale:
                  </div>
                  <div style={{ color: '#667eea', fontSize: '1.1rem', fontWeight: '600' }}>
                    {topPrediction?.breed || 'N/A'}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default ModelComparison;

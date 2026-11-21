import ConfidenceBar from './ConfidenceBar';

function getCategoryStyle(category) {
  const c = (category || '').toLowerCase();
  if (c.includes('wet') || c.includes('organic')) return 'wet';
  if (c.includes('dry') || c.includes('recyclable')) return 'dry';
  if (c.includes('mixed')) return 'mixed';
  if (c.includes('segregated') || c.includes('properly')) return 'segregated';
  return 'uncertain';
}

export default function PredictionResult({ result, imageUrl }) {
  if (!result) return null;

  // Normalize API and hook output structures
  const predictedCategory = result.predicted_category || result.predicted_class || 'Uncertain';
  const confidenceVal = result.confidence_score !== undefined ? result.confidence_score : (result.confidence !== undefined ? result.confidence : 0);
  const modeVal = result.classification_mode || result.mode || 'item';
  const modelName = result.model_name || 'MobileNetV2';
  const timestamp = result.timestamp || result.created_at || new Date().toISOString();
  const probabilities = result.probabilities || {};

  const style = getCategoryStyle(predictedCategory);
  const confidencePct = typeof confidenceVal === 'number'
    ? (confidenceVal > 1 ? confidenceVal : confidenceVal * 100).toFixed(1)
    : parseFloat(confidenceVal || 0).toFixed(1);

  return (
    <div className="prediction-result animate-slide-up">
      <div className={`prediction-result__header prediction-result__header--${style}`}>
        <div className="prediction-result__category">{predictedCategory}</div>
        <div className="prediction-result__confidence">{confidencePct}%</div>
        <div style={{ fontSize: 'var(--font-size-sm)', opacity: 0.85 }}>Confidence</div>
      </div>

      <div className="prediction-result__body">
        {imageUrl && (
          <div style={{ textAlign: 'center', marginBottom: 'var(--space-4)' }}>
            <img 
              src={imageUrl} 
              alt="Uploaded Waste" 
              style={{ maxWidth: '200px', maxHeight: '180px', borderRadius: 'var(--radius-md)', objectFit: 'cover', border: '2px solid var(--border-color)' }} 
            />
          </div>
        )}

        <ConfidenceBar value={parseFloat(confidencePct)} label="Confidence" />

        {parseFloat(confidencePct) < 60 && (
          <div className="uncertainty-msg">
            <span className="uncertainty-msg__icon">⚠️</span>
            <div>
              <strong>Low confidence or insufficient visual evidence.</strong> The model is not sufficiently certain about this classification. Consider uploading a clearer, well-lit image.
            </div>
          </div>
        )}

        <div className="prediction-result__meta">
          <span className="prediction-result__meta-item">
            📋 Mode: {modeVal === 'item' ? 'Individual Item Analysis' : 'Segregation Scene Analysis'}
          </span>
          <span className="prediction-result__meta-item">
            🧠 Model: {modelName}
          </span>
          <span className="prediction-result__meta-item">
            🕐 {new Date(timestamp).toLocaleString()}
          </span>
        </div>
      </div>
    </div>
  );
}

import { useLocation, useNavigate, Link } from 'react-router-dom';
import PredictionResult from '../components/classification/PredictionResult';
import ProbabilityChart from '../components/classification/ProbabilityChart';
import Button from '../components/common/Button';

export default function Results() {
  const location = useLocation();
  const navigate = useNavigate();
  const state = location.state;

  if (!state || !state.result) {
    return (
      <div className="container" style={{ padding: 'var(--space-16) var(--space-4)', textAlign: 'center' }}>
        <h2>No Active Result Found</h2>
        <p style={{ color: 'var(--color-text-secondary)', margin: 'var(--space-4) 0 var(--space-6)' }}>
          Please upload and classify an image first to view prediction results.
        </p>
        <Link to="/classify">
          <Button variant="primary">Go to Classifier</Button>
        </Link>
      </div>
    );
  }

  const { result, imageUrl, mode } = state;
  const probabilities = result.probabilities || {};

  return (
    <div className="container animate-fade-in" style={{ padding: 'var(--space-10) var(--space-4)', maxWidth: '780px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-6)' }}>
        <h1 style={{ fontSize: 'var(--font-size-2xl)', fontWeight: 'bold' }}>Classification Results</h1>
        <Button variant="outline" size="sm" onClick={() => navigate(mode === 'segregation' ? '/classify/segregation' : '/classify/item')}>
          ➕ Classify Another
        </Button>
      </div>

      {/* Main Result Card */}
      <PredictionResult result={result} imageUrl={imageUrl} />

      {/* Probability Chart */}
      {Object.keys(probabilities).length > 0 && (
        <div className="card" style={{ marginTop: 'var(--space-6)' }}>
          <ProbabilityChart probabilities={probabilities} />
        </div>
      )}

      {/* Practical Disposal Guidance */}
      <div className="card" style={{ marginTop: 'var(--space-6)', background: 'var(--color-bg-alt)' }}>
        <h3 style={{ fontSize: 'var(--font-size-base)', fontWeight: 'bold', marginBottom: 'var(--space-2)' }}>
          💡 Practical Segregation & Disposal Advice
        </h3>
        <p style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-secondary)', lineHeight: 'var(--line-height-relaxed)', margin: 0 }}>
          {result.predicted_category === 'Wet' || result.predicted_class === 'Wet'
            ? 'Place this item in the Green Bin. Wet waste should be composted locally or collected for municipal biogas/anaerobic digestion. Avoid mixing in plastic packaging.'
            : result.predicted_category === 'Dry' || result.predicted_class === 'Dry'
            ? 'Place this item in the Blue Bin. Ensure items are rinsed clean and free from organic residue before handing over to authorized dry waste recyclers.'
            : result.predicted_category === 'Mixed Waste' || result.predicted_class === 'Mixed Waste'
            ? 'Improper segregation detected. Wet kitchen organics and dry recyclables must be physically separated into green and blue bins prior to waste handover.'
            : 'Proper segregation verified. Green and blue streams are distinct and contamination-free. Ready for municipal pickup.'}
        </p>
      </div>

      <div style={{ marginTop: 'var(--space-8)', display: 'flex', gap: 'var(--space-4)', justifyContent: 'center' }}>
        <Button variant="primary" onClick={() => navigate('/classify')}>
          Classify Another Image
        </Button>
        <Link to="/model-info">
          <Button variant="secondary">View Model Diagnostics</Button>
        </Link>
      </div>
    </div>
  );
}


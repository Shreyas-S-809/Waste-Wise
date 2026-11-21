export default function ConfidenceBar({ value, label }) {
  const level = value >= 80 ? 'high' : value >= 50 ? 'medium' : 'low';

  return (
    <div className="confidence-bar">
      <div className="confidence-bar__label">
        <span>{label || 'Confidence'}</span>
        <span>{value.toFixed(1)}%</span>
      </div>
      <div className="confidence-bar__track">
        <div
          className={`confidence-bar__fill confidence-bar__fill--${level}`}
          style={{ width: `${Math.min(value, 100)}%` }}
        />
      </div>
    </div>
  );
}

import { useState, useEffect } from 'react';
import { getModelsStatus } from '../api/prediction';

export default function ModelInfo() {
  const [modelStatus, setModelStatus] = useState(null);

  useEffect(() => {
    getModelsStatus()
      .then((res) => setModelStatus(res.data || res))
      .catch(() => {});
  }, []);

  return (
    <div className="animate-fade-in" style={{ height: '100%', display: 'flex', flexDirection: 'column', gap: '12px', overflow: 'hidden' }}>
      {/* Metrics Row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '12px', flexShrink: 0 }}>
        <div className="metric-card" style={{ padding: '10px 14px' }}>
          <div className="metric-label" style={{ fontSize: '11px', fontWeight: 600, letterSpacing: '0.05em', marginBottom: '4px' }}>Decisive Test Accuracy</div>
          <div className="metric-value" style={{ fontSize: '24px', fontWeight: 700, color: 'var(--accent-green)' }}>90.2%</div>
          <div className="metric-subtext" style={{ fontSize: '11.5px', marginTop: '3px' }}>Verified on independent test set</div>
        </div>

        <div className="metric-card" style={{ padding: '10px 14px' }}>
          <div className="metric-label" style={{ fontSize: '11px', fontWeight: 600, letterSpacing: '0.05em', marginBottom: '4px' }}>Overall Test Accuracy</div>
          <div className="metric-value" style={{ fontSize: '24px', fontWeight: 700 }}>88.0%</div>
          <div className="metric-subtext" style={{ fontSize: '11.5px', color: 'var(--text-secondary)', marginTop: '3px' }}>Macro F1: 0.88</div>
        </div>

        <div className="metric-card" style={{ padding: '10px 14px' }}>
          <div className="metric-label" style={{ fontSize: '11px', fontWeight: 600, letterSpacing: '0.05em', marginBottom: '4px' }}>Dry Waste Precision</div>
          <div className="metric-value" style={{ fontSize: '24px', fontWeight: 700, color: 'var(--accent-blue)' }}>92.0%</div>
          <div className="metric-subtext" style={{ fontSize: '11.5px', color: 'var(--accent-blue)', marginTop: '3px' }}>Recall: 83.0% | F1: 0.87</div>
        </div>

        <div className="metric-card" style={{ padding: '10px 14px' }}>
          <div className="metric-label" style={{ fontSize: '11px', fontWeight: 600, letterSpacing: '0.05em', marginBottom: '4px' }}>Wet Waste Recall</div>
          <div className="metric-value" style={{ fontSize: '24px', fontWeight: 700, color: 'var(--accent-green)' }}>93.0%</div>
          <div className="metric-subtext" style={{ fontSize: '11.5px', color: 'var(--text-secondary)', marginTop: '3px' }}>Precision: 85.0% | F1: 0.89</div>
        </div>
      </div>

      {/* Main Grid: Confusion Matrix & Architecture */}
      <div style={{ flex: 1, minHeight: 0, display: 'grid', gridTemplateColumns: '1.15fr 1fr', gap: '14px' }}>
        {/* Confusion Matrix Card */}
        <div className="card-dark" style={{ padding: '14px 16px', display: 'flex', flexDirection: 'column', minHeight: 0, overflow: 'hidden' }}>
          <div style={{ fontSize: '15px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px', flexShrink: 0 }}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="3" y1="9" x2="21" y2="9"></line>
              <line x1="9" y1="21" x2="9" y2="9"></line>
            </svg>
            <span>Normalized Confusion Matrix</span>
          </div>

          <div style={{ flex: 1, minHeight: 0, width: '100%', borderRadius: 'var(--radius-sm)', overflow: 'hidden', backgroundColor: 'var(--bg-primary)', display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px solid var(--border-subtle)', padding: '6px' }}>
            <img
              src="/confusion_matrix_wet_dry.png"
              alt="Confusion matrix heatmap"
              style={{ maxHeight: '100%', maxWidth: '100%', height: '100%', objectFit: 'contain' }}
              onError={(e) => {
                e.target.style.display = 'none';
                e.target.parentElement.innerHTML = '<div style="color:var(--text-muted);font-size:12px;padding:12px;text-align:center;">Confusion matrix plot saved to models/evaluation/confusion_matrix_wet_dry.png</div>';
              }}
            />
          </div>
        </div>

        {/* Technical Architecture Specs */}
        <div className="card-dark" style={{ padding: '14px 16px', display: 'flex', flexDirection: 'column', minHeight: 0, overflow: 'hidden' }}>
          <div style={{ fontSize: '15px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px', flexShrink: 0 }}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
            <span>Model Engineering Specs</span>
          </div>

          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'space-between', fontSize: '12.5px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '5px 0', borderBottom: '1px solid var(--border-subtle)' }}>
              <span style={{ color: 'var(--text-secondary)' }}>Base Architecture</span>
              <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--text-primary)', fontWeight: 500 }}>MobileNetV2 (ImageNet)</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '5px 0', borderBottom: '1px solid var(--border-subtle)' }}>
              <span style={{ color: 'var(--text-secondary)' }}>Input Dimensions</span>
              <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--text-primary)', fontWeight: 500 }}>224 × 224 × 3 (RGB)</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '5px 0', borderBottom: '1px solid var(--border-subtle)' }}>
              <span style={{ color: 'var(--text-secondary)' }}>Normalization</span>
              <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--text-primary)', fontWeight: 500 }}>[-1.0, 1.0] (Pixel / 127.5 - 1)</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '5px 0', borderBottom: '1px solid var(--border-subtle)' }}>
              <span style={{ color: 'var(--text-secondary)' }}>Confidence Threshold</span>
              <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--text-primary)', fontWeight: 500 }}>≥ 60% with ≥ 15% margin</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '5px 0', borderBottom: '1px solid var(--border-subtle)' }}>
              <span style={{ color: 'var(--text-secondary)' }}>Out-of-Distribution Guard</span>
              <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--accent-green)', fontWeight: 600 }}>Texture std ≥ 12.0</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '5px 0' }}>
              <span style={{ color: 'var(--text-secondary)' }}>Active Model File</span>
              <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--text-primary)', fontWeight: 500 }}>wet_dry_mobilenetv2.keras</span>
            </div>
          </div>
        </div>
      </div>

      {/* Dataset Mapping Specifications */}
      <div className="card-dark" style={{ padding: '12px 16px', flexShrink: 0 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '8px' }}>
          <div style={{ fontSize: '15px', fontWeight: 600, color: 'var(--text-primary)' }}>
            Dataset Ingestion & Label Alignment
          </div>
          <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
            Stratified 70/15/15 split across TechSash and RealWaste (29,016 verified images)
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '12px' }}>
          <div style={{ padding: '8px 12px', backgroundColor: 'var(--bg-surface-secondary)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
            <strong style={{ fontSize: '13.5px', color: 'var(--accent-blue)', display: 'block', marginBottom: '3px' }}>Dry Waste Classes</strong>
            <p style={{ fontSize: '12px', color: 'var(--text-secondary)', lineHeight: 1.45 }}>TechSash Recyclable, RealWaste Cardboard, Glass, Metal, Paper, and Plastic.</p>
          </div>
          <div style={{ padding: '8px 12px', backgroundColor: 'var(--bg-surface-secondary)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
            <strong style={{ fontSize: '13.5px', color: 'var(--accent-green)', display: 'block', marginBottom: '3px' }}>Wet Waste Classes</strong>
            <p style={{ fontSize: '12px', color: 'var(--text-secondary)', lineHeight: 1.45 }}>TechSash Organic, RealWaste Food Organics, and Biodegradable Vegetation.</p>
          </div>
          <div style={{ padding: '8px 12px', backgroundColor: 'var(--bg-surface-secondary)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
            <strong style={{ fontSize: '13.5px', color: 'var(--accent-amber)', display: 'block', marginBottom: '3px' }}>Excluded Ambiguities</strong>
            <p style={{ fontSize: '12px', color: 'var(--text-secondary)', lineHeight: 1.45 }}>Textile & Miscellaneous Trash excluded to guarantee label validity.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
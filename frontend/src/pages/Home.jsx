import { useNavigate } from 'react-router-dom';

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="animate-fade-in" style={{ height: '100%', display: 'flex', flexDirection: 'column', gap: '14px', overflow: 'hidden' }}>
      {/* Hero Quick-Start Card */}
      <div className="card-dark" style={{ padding: '20px 24px', flex: '1.2', display: 'flex', flexDirection: 'column', justifyContent: 'center', background: 'linear-gradient(135deg, rgba(22, 163, 106, 0.09) 0%, rgba(17, 17, 20, 1) 100%)', border: '1px solid var(--border-subtle)', minHeight: 0 }}>
        <div style={{ maxWidth: '680px' }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', padding: '3px 9px', borderRadius: 'var(--radius-full)', background: 'var(--accent-green-subtle)', border: '1px solid var(--accent-green-border)', color: 'var(--accent-green)', fontSize: '11px', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '8px' }}>
            <span>● Production Ready</span>
          </div>

          <h2 style={{ fontSize: '24px', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '8px', letterSpacing: '-0.02em', lineHeight: 1.25 }}>
            AI-Powered Waste Classification System
          </h2>

          <p style={{ fontSize: '14px', color: 'var(--text-secondary)', lineHeight: 1.55, marginBottom: '16px' }}>
            WasteWise leverages MobileNetV2 transfer learning with confidence calibration to separate organic compostable waste from recyclables in real-time.
          </p>

          <div style={{ display: 'flex', gap: '12px' }}>
            <button
              className="btn-primary"
              style={{ width: 'auto', padding: '8px 20px', fontSize: '14px', fontWeight: 600 }}
              onClick={() => navigate('/classify')}
            >
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                <polygon points="5 3 19 12 5 21 5 3"></polygon>
              </svg>
              <span>Launch Classifier</span>
            </button>

            <button
              className="btn-secondary"
              style={{ padding: '8px 18px', fontSize: '14px', fontWeight: 500 }}
              onClick={() => navigate('/model-info')}
            >
              <span>View Diagnostics</span>
            </button>
          </div>
        </div>
      </div>

      {/* Feature Dimension Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '14px', flex: '1', minHeight: 0 }}>
        <div
          className="card-dark card-dark--hover"
          style={{ cursor: 'pointer', padding: '16px 20px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}
          onClick={() => navigate('/classify?mode=item')}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
            <span style={{ fontSize: '22px' }}>🌱</span>
            <span style={{ fontSize: '11px', fontWeight: 600, color: 'var(--accent-green)', backgroundColor: 'var(--accent-green-subtle)', border: '1px solid var(--accent-green-border)', padding: '2px 8px', borderRadius: 'var(--radius-full)' }}>
              MODEL A ACTIVE
            </span>
          </div>
          <h3 style={{ fontSize: '16.5px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '6px' }}>
            Individual Waste Item Analysis
          </h3>
          <p style={{ fontSize: '13.5px', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
            Classifies single items as Organic / Wet (vegetable peels, leftover food, compostables) or Dry (paper, plastic, metal cans, glass).
          </p>
        </div>

        <div
          className="card-dark card-dark--hover"
          style={{ cursor: 'pointer', padding: '16px 20px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}
          onClick={() => navigate('/classify?mode=segregation')}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
            <span style={{ fontSize: '22px' }}>♻️</span>
            <span style={{ fontSize: '11px', fontWeight: 600, color: 'var(--accent-amber)', backgroundColor: 'var(--accent-amber-subtle)', border: '1px solid var(--accent-amber-border)', padding: '2px 8px', borderRadius: 'var(--radius-full)' }}>
              MODEL B PENDING
            </span>
          </div>
          <h3 style={{ fontSize: '16.5px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '6px' }}>
            Segregation Scene Auditor
          </h3>
          <p style={{ fontSize: '13.5px', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
            Evaluates multi-bin collection points and dual-compartment bins for proper segregation compliance versus unsegregated mixed waste.
          </p>
        </div>
      </div>

      {/* Highlights Row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '14px', flexShrink: 0 }}>
        <div className="card-dark" style={{ padding: '14px 18px' }}>
          <div style={{ fontSize: '11.5px', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '4px' }}>Accuracy Rate</div>
          <div style={{ fontSize: '24px', fontWeight: 700, fontFamily: 'var(--font-mono)', color: 'var(--accent-green)' }}>90.2%</div>
          <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '2px' }}>On decisive test inferences</div>
        </div>

        <div className="card-dark" style={{ padding: '14px 18px' }}>
          <div style={{ fontSize: '11.5px', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '4px' }}>Image Processing</div>
          <div style={{ fontSize: '24px', fontWeight: 700, fontFamily: 'var(--font-mono)', color: 'var(--text-primary)' }}>224 × 224</div>
          <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '2px' }}>RGB MobileNetV2 tensor</div>
        </div>

        <div className="card-dark" style={{ padding: '14px 18px' }}>
          <div style={{ fontSize: '11.5px', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '4px' }}>Auditing Storage</div>
          <div style={{ fontSize: '24px', fontWeight: 700, fontFamily: 'var(--font-mono)', color: 'var(--accent-blue)' }}>SQLite DB</div>
          <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '2px' }}>Persistent local audit trail</div>
        </div>
      </div>
    </div>
  );
}
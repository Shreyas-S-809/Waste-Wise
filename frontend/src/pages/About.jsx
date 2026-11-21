export default function About() {
  return (
    <div className="animate-fade-in" style={{ height: '100%', display: 'flex', flexDirection: 'column', gap: '12px', overflow: 'hidden' }}>
      <div className="card-dark" style={{ padding: '16px 20px', flex: '1.1', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', minHeight: 0 }}>
        <div>
          <h2 style={{ fontSize: '18px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '6px' }}>
            WasteWise System Overview
          </h2>
          <p style={{ fontSize: '13.5px', color: 'var(--text-secondary)', lineHeight: 1.55 }}>
            WasteWise is an automated computer vision application designed to address municipal solid waste (MSW) segregation challenges. By combining MobileNetV2 transfer learning, calibrated confidence scoring, and strict dataset curation, WasteWise accurately distinguishes between organic compostable waste (Wet) and recyclable material streams (Dry).
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px', marginTop: '10px' }}>
          <div style={{ padding: '10px 14px', backgroundColor: 'var(--bg-surface-secondary)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '11px', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '4px' }}>Architecture</div>
            <div style={{ fontSize: '15px', fontWeight: 600, color: 'var(--text-primary)' }}>MobileNetV2 CNN</div>
            <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '2px' }}>ImageNet Transfer Learning</div>
          </div>

          <div style={{ padding: '10px 14px', backgroundColor: 'var(--bg-surface-secondary)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '11px', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '4px' }}>Inference Engine</div>
            <div style={{ fontSize: '15px', fontWeight: 600, color: 'var(--text-primary)' }}>TensorFlow / Keras</div>
            <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '2px' }}>RESTful Python Backend</div>
          </div>

          <div style={{ padding: '10px 14px', backgroundColor: 'var(--bg-surface-secondary)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '11px', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '4px' }}>Verified Benchmark</div>
            <div style={{ fontSize: '15px', fontWeight: 600, color: 'var(--text-primary)' }}>TechSash & RealWaste</div>
            <div style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '2px' }}>29,016 Stratified Samples</div>
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', flex: '1', minHeight: 0 }}>
        <div className="card-dark" style={{ padding: '16px 20px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <h3 style={{ fontSize: '16px', fontWeight: 600, marginBottom: '6px', color: 'var(--accent-green)' }}>
            Model A — Waste Type Classifier
          </h3>
          <p style={{ fontSize: '13.5px', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
            Focuses strictly on individual object classification. Determines whether an individual object presented in the frame belongs to organic biodegradable matter (kitchen scraps, vegetables, fruit peels) or non-biodegradable recyclables (bottles, paper, plastics, metals).
          </p>
        </div>

        <div className="card-dark" style={{ padding: '16px 20px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <h3 style={{ fontSize: '16px', fontWeight: 600, marginBottom: '6px', color: 'var(--accent-blue)' }}>
            Model B — Segregation Status Auditor
          </h3>
          <p style={{ fontSize: '13.5px', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
            Audits multi-bin collection points and dual-compartment bins for proper segregation compliance (Mixed Waste vs. Properly Segregated). Prevents naive single-item false positives by isolating scene-level visual evidence.
          </p>
        </div>
      </div>

      <div className="card-dark" style={{ padding: '14px 20px', flexShrink: 0 }}>
        <h3 style={{ fontSize: '15px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '4px' }}>
          Scientific Rigor & Uncertainty Handling
        </h3>
        <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: 1.45 }}>
          Rather than forcing low-confidence predictions into random classifications, WasteWise employs probability margin calibration (threshold ≥ 60%, margin ≥ 15%) and visual entropy checks. Ambiguous images or out-of-distribution inputs receive an explicit <em>Uncertain</em> flag with instructions to re-photograph or manually inspect.
        </p>
      </div>
    </div>
  );
}
import ClassificationCard from '../components/classification/ClassificationCard';

export default function ModeSelection() {
  return (
    <div className="container animate-fade-in" style={{ padding: 'var(--space-12) var(--space-4)', maxWidth: '900px' }}>
      <div style={{ textAlign: 'center', marginBottom: 'var(--space-10)' }}>
        <h1 style={{ fontSize: 'var(--font-size-3xl)', fontWeight: 'bold', color: 'var(--color-primary-900)' }}>
          Select Classification Mode
        </h1>
        <p style={{ color: 'var(--color-text-secondary)', maxWidth: '600px', margin: 'var(--space-2) auto 0' }}>
          Please select the analysis mode corresponding to your input photograph. WasteWise applies specialized deep learning models tailored for each visual task.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: 'var(--space-8)' }}>
        <ClassificationCard
          to="/classify/item"
          icon="🍎"
          title="Individual Waste Item Analysis"
          description="Identify whether an individual piece of household waste is Wet (organic, biodegradable kitchen waste) or Dry (recyclable plastic, paper, metal, cardboard, glass). Uses Model A (MobileNetV2 Wet/Dry Classifier)."
        />

        <ClassificationCard
          to="/classify/segregation"
          icon="🗑️"
          title="Waste Bin / Segregation Scene"
          description="Analyze a waste collection receptacle or collection point to verify if waste has been Properly Segregated into respective streams or remains Mixed Waste. Uses Model B (Segregation Status Classifier)."
        />
      </div>

      <div style={{ marginTop: 'var(--space-10)', padding: 'var(--space-5)', background: 'var(--color-bg-alt)', borderRadius: 'var(--radius-lg)', textAlign: 'center' }}>
        <p style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-secondary)', margin: 0 }}>
          💡 <strong>Engineering Note:</strong> A single object photograph (e.g. banana peel) tests waste material type, not household compliance. Choose <em>Bin / Segregation Scene</em> for multi-bin compliance inspection.
        </p>
      </div>
    </div>
  );
}


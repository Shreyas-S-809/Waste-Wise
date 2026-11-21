export default function HowItWorks() {
  return (
    <div className="container animate-fade-in" style={{ padding: 'var(--space-12) var(--space-4)', maxWidth: '900px' }}>
      <div style={{ textAlign: 'center', marginBottom: 'var(--space-10)' }}>
        <h1 style={{ fontSize: 'var(--font-size-3xl)', fontWeight: 'bold', color: 'var(--color-primary-900)' }}>
          How WasteWise Works
        </h1>
        <p style={{ color: 'var(--color-text-secondary)', maxWidth: '650px', margin: 'var(--space-2) auto 0' }}>
          An end-to-end overview of the visual processing, Convolutional Neural Network (CNN) feature extraction, and transfer learning inference architecture.
        </p>
      </div>

      {/* Visual Flowchart */}
      <div className="card" style={{ marginBottom: 'var(--space-10)', padding: 'var(--space-8)' }}>
        <h2 style={{ fontSize: 'var(--font-size-xl)', fontWeight: 'bold', textAlign: 'center', marginBottom: 'var(--space-6)' }}>
          Visual Processing Pipeline
        </h2>

        <div className="flowchart">
          <div className="flowchart__node">
            1. Image Capture & Upload (JPEG, PNG, WebP)
          </div>
          <div className="flowchart__arrow">↓</div>
          <div className="flowchart__node">
            2. Preprocessing: Resizing to 224 × 224 & MobileNetV2 Scale ([-1, 1])
          </div>
          <div className="flowchart__arrow">↓</div>
          <div className="flowchart__node flowchart__node--highlight">
            3. MobileNetV2 Pretrained Convolutional Feature Extractor
          </div>
          <div className="flowchart__arrow">↓</div>
          <div className="flowchart__node">
            4. Global Average Pooling 2D + Dropout (0.3) Regularization
          </div>
          <div className="flowchart__arrow">↓</div>
          <div className="flowchart__node">
            5. Dense Classification Head + Softmax Probability Distribution
          </div>
          <div className="flowchart__arrow">↓</div>
          <div className="flowchart__node">
            6. Confidence Calibration Thresholding (τ = 0.60)
          </div>
          <div className="flowchart__arrow">↓</div>
          <div className="flowchart__node" style={{ borderColor: 'var(--color-primary-700)', background: 'var(--color-bg-light)' }}>
            7. Verified Output: Category + Calibrated Confidence + SQLite History Record
          </div>
        </div>
      </div>

      {/* Detailed Technical Sections */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 'var(--space-6)' }}>
        <div className="card">
          <h3 style={{ fontSize: 'var(--font-size-lg)', fontWeight: 'bold', marginBottom: 'var(--space-3)', color: 'var(--color-primary-800)' }}>
            1. Why MobileNetV2?
          </h3>
          <p style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-secondary)', lineHeight: 'var(--line-height-relaxed)' }}>
            MobileNetV2 employs inverted residual blocks with depthwise separable convolutions and linear bottlenecks. This architecture delivers high top-1 visual classification accuracy while keeping parameters lightweight (~3.5M parameters), enabling near instantaneous inference on consumer hardware and low-power edge nodes.
          </p>
        </div>

        <div className="card">
          <h3 style={{ fontSize: 'var(--font-size-lg)', fontWeight: 'bold', marginBottom: 'var(--space-3)', color: 'var(--color-primary-800)' }}>
            2. Transfer Learning Strategy
          </h3>
          <p style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-secondary)', lineHeight: 'var(--line-height-relaxed)' }}>
            Initial layers capture universal visual features (edges, textures, gradients) from ImageNet. We freeze the base feature extractor during initial head training, followed by fine-tuning top convolutional layers at a reduced learning rate (1e-5) to adapt high-level feature representations to solid waste textures.
          </p>
        </div>

        <div className="card">
          <h3 style={{ fontSize: 'var(--font-size-lg)', fontWeight: 'bold', marginBottom: 'var(--space-3)', color: 'var(--color-primary-800)' }}>
            3. Two Classification Dimensions
          </h3>
          <p style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-secondary)', lineHeight: 'var(--line-height-relaxed)' }}>
            <strong>Model A (Item Level):</strong> Evaluates physical material properties (biodegradable organic vs non-biodegradable recyclable).<br />
            <strong>Model B (Segregation Level):</strong> Evaluates compliance of the containment scene (segregated streams vs contaminated/mixed bins).
          </p>
        </div>

        <div className="card">
          <h3 style={{ fontSize: 'var(--font-size-lg)', fontWeight: 'bold', marginBottom: 'var(--space-3)', color: 'var(--color-primary-800)' }}>
            4. Reliability & Uncertainty
          </h3>
          <p style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-secondary)', lineHeight: 'var(--line-height-relaxed)' }}>
            High softmax scores do not guarantee ground truth on out-of-distribution inputs. WasteWise implements a strict confidence threshold check. When confidence falls below 60%, the system flags the result with an insufficient visual evidence alert rather than outputting a deceptive classification.
          </p>
        </div>
      </div>
    </div>
  );
}


import { useState, useRef, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import usePrediction from '../hooks/usePrediction';

export default function Classifier() {
  const [searchParams, setSearchParams] = useSearchParams();
  const currentMode = searchParams.get('mode') === 'segregation' ? 'segregation' : 'item';

  const { classify, loading, error, result, reset } = usePrediction(currentMode);

  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  // Clear file & result on mode change
  useEffect(() => {
    handleClear();
  }, [currentMode]);

  const handleModeChange = (mode) => {
    setSearchParams({ mode });
  };

  const handleFileSelect = (file) => {
    if (!file) return;
    if (!file.type.startsWith('image/')) {
      alert('Please upload a valid image file (JPEG, PNG, WebP).');
      return;
    }
    setSelectedFile(file);
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
    reset();
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleClear = () => {
    setSelectedFile(null);
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
      setPreviewUrl(null);
    }
    reset();
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSubmit = async () => {
    if (!selectedFile || loading) return;
    try {
      await classify(selectedFile);
    } catch {
      // error is handled in hook
    }
  };

  // Helper for category badge styling
  const getCategoryClass = (category, status) => {
    if (status === 'UNCERTAIN' || category === 'Uncertain') return 'uncertain';
    if (category === 'Wet' || category === 'Properly Segregated') return 'wet';
    return 'dry';
  };

  // Extract result data (response may be nested in `data` by axios wrapper)
  const data = result?.data || result;
  const isItem = currentMode === 'item';

  return (
    <div className="classifier-workspace animate-fade-in">
      {/* LEFT COLUMN: Input & Upload Workspace */}
      <div className="workspace-panel">
        <div className="workspace-panel__header">
          <div className="workspace-panel__title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="17 8 12 3 7 8"></polyline>
              <line x1="12" y1="3" x2="12" y2="15"></line>
            </svg>
            <span>Image Input</span>
          </div>

          {selectedFile && (
            <button className="btn-secondary" onClick={handleClear} disabled={loading}>
              Reset
            </button>
          )}
        </div>

        <div className="workspace-panel__body">
          {/* Mode Switcher Tabs with Morphing Sliding Pill */}
          <div className="mode-tabs">
            <div
              className="mode-tabs__pill"
              style={{
                transform: isItem ? 'translateX(0%)' : 'translateX(100%)',
              }}
            />
            <button
              type="button"
              className={`mode-tab ${isItem ? 'mode-tab--active' : ''}`}
              onClick={() => handleModeChange('item')}
            >
              Mode A: Waste Item
            </button>
            <button
              type="button"
              className={`mode-tab ${!isItem ? 'mode-tab--active' : ''}`}
              onClick={() => handleModeChange('segregation')}
            >
              Mode B: Segregation Scene
            </button>
          </div>

          {!isItem && (
            <div className="alert-box alert-box--warning" style={{ marginBottom: '14px' }}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
              <div>
                <strong>Phase 2 Curated Model Notice:</strong> Model B (Segregation Status Classifier) is currently in training/curation. Individual Item classification is active.
              </div>
            </div>
          )}

          <input
            ref={fileInputRef}
            type="file"
            accept="image/jpeg,image/png,image/webp"
            style={{ display: 'none' }}
            onChange={(e) => handleFileSelect(e.target.files[0])}
          />

          {!selectedFile ? (
            <div
              className={`upload-dropzone ${dragActive ? 'upload-dropzone--active' : ''}`}
              onClick={() => fileInputRef.current?.click()}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <div className="upload-dropzone__icon">
                <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                  <circle cx="8.5" cy="8.5" r="1.5"></circle>
                  <polyline points="21 15 16 10 5 21"></polyline>
                </svg>
              </div>
              <div className="upload-dropzone__title">
                Choose a photograph or drag & drop here
              </div>
              <div className="upload-dropzone__subtitle">
                JPG, PNG, WebP up to 10MB
              </div>
            </div>
          ) : (
            <div className="preview-container">
              <div className="preview-image-box">
                <img src={previewUrl} alt="Waste item preview" />
              </div>

              <div className="preview-meta">
                <span style={{ textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap', maxWidth: '200px' }}>
                  {selectedFile.name}
                </span>
                <span>{(selectedFile.size / 1024).toFixed(1)} KB</span>
              </div>

              <button
                className="btn-primary"
                onClick={handleSubmit}
                disabled={loading}
              >
                {loading ? (
                  <>
                    <svg className="animate-spin" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <circle cx="12" cy="12" r="10" strokeDasharray="32" strokeDashoffset="12"></circle>
                    </svg>
                    <span>Evaluating Visual Features...</span>
                  </>
                ) : (
                  <>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <polygon points="5 3 19 12 5 21 5 3"></polygon>
                    </svg>
                    <span>Classify Waste Image</span>
                  </>
                )}
              </button>
            </div>
          )}

          {error && (
            <div className="alert-box alert-box--warning" style={{ marginTop: '14px' }}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2"></polygon>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
              <div>{typeof error === 'object' ? (error?.message || JSON.stringify(error)) : String(error)}</div>
            </div>
          )}
        </div>
      </div>

      {/* RIGHT COLUMN: Inference Analysis & Results */}
      <div className="workspace-panel">
        <div className="workspace-panel__header">
          <div className="workspace-panel__title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
            </svg>
            <span>Classification Results & Analysis</span>
          </div>

          {data && (
            <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
              {data.model_name}
            </span>
          )}
        </div>

        <div className="workspace-panel__body">
          {!data && !loading && (
            <div className="empty-state">
              <div className="empty-state__icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
              </div>
              <div className="empty-state__title">Awaiting Waste Photograph</div>
              <div className="empty-state__description">
                Upload or drop an image on the left to extract visual features and classify waste.
              </div>
            </div>
          )}

          {loading && (
            <div className="empty-state">
              <div className="empty-state__icon" style={{ animation: 'spin 1s linear infinite' }}>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 12a9 9 0 1 1-6.219-8.56"></path>
                </svg>
              </div>
              <div className="empty-state__title">MobileNetV2 Inference In Progress</div>
              <div className="empty-state__description">
                Preprocessing 224x224 RGB tensor and computing class probabilities...
              </div>
            </div>
          )}

          {data && !loading && (
            <div>
              {/* Primary Header Card */}
              <div className={`result-header-card result-header-card--${getCategoryClass(data.predicted_category, data.status)}`}>
                <div className="result-title-group">
                  <span className={`result-badge result-badge--${getCategoryClass(data.predicted_category, data.status)}`}>
                    {data.status === 'UNCERTAIN' ? 'Uncertain / Ambiguous' : 'Confirmed Prediction'}
                  </span>
                  <div className="result-class-name">
                    {data.predicted_category === 'Uncertain' ? 'Insufficient Evidence' : `${data.predicted_category} Waste`}
                  </div>
                </div>

                <div className="result-confidence-box">
                  <div className="result-confidence-number">
                    {(data.confidence_score * 100).toFixed(1)}%
                  </div>
                  <div className="result-confidence-label">Confidence</div>
                </div>
              </div>

              {/* Warning Notice if Low Confidence or Uncertain */}
              {data.warning && (
                <div className="alert-box alert-box--warning">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ flexShrink: 0, marginTop: '2px' }}>
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="12"></line>
                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                  </svg>
                  <div>{data.warning}</div>
                </div>
              )}

              {/* Probability Breakdown Card */}
              {data.probabilities && (
                <div className="probabilities-card">
                  <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '12px' }}>
                    Class Probabilities Breakdown
                  </div>

                  {Object.entries(data.probabilities).map(([className, prob]) => {
                    const isDry = className.toLowerCase().includes('dry');
                    const percent = (prob * 100).toFixed(1);

                    return (
                      <div key={className} className="prob-item">
                        <div className="prob-header">
                          <span className="prob-label">{className} Waste</span>
                          <span className="prob-value">{percent}%</span>
                        </div>
                        <div className="prob-track">
                          <div
                            className={`prob-fill ${isDry ? 'prob-fill--dry' : 'prob-fill--wet'}`}
                            style={{ width: `${percent}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}

              {/* Disposal Advice Guidance Card */}
              <div className="guidance-card">
                <div className="guidance-icon">
                  {data.predicted_category === 'Wet' ? '🌱' : data.predicted_category === 'Dry' ? '♻️' : '⚠️'}
                </div>
                <div>
                  <div className="guidance-title">Disposal Guidance</div>
                  <div className="guidance-text">{data.disposal_advice}</div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

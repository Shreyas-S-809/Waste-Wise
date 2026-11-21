import { useState, useEffect } from 'react';
import UploadZone from './UploadZone';
import ImagePreview from './ImagePreview';
import Button from '../common/Button';

export default function ImageUploader({ onClassify, loading }) {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);

  useEffect(() => {
    if (!file) {
      setPreviewUrl(null);
      return;
    }
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);

  const handleRemove = () => {
    setFile(null);
    setPreviewUrl(null);
  };

  const handleClassify = () => {
    if (file) onClassify(file);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-6)' }}>
      {!file ? (
        <UploadZone onFileSelect={setFile} />
      ) : (
        <ImagePreview file={file} previewUrl={previewUrl} onRemove={handleRemove} />
      )}

      {file && (
        <Button
          variant="primary"
          size="lg"
          full
          loading={loading}
          onClick={handleClassify}
          disabled={loading}
        >
          {loading ? 'Classifying…' : '🔍 Classify Image'}
        </Button>
      )}
    </div>
  );
}

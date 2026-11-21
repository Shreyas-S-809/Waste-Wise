import { useState, useRef } from 'react';

const ACCEPTED_TYPES = ['image/jpeg', 'image/png', 'image/webp', 'image/bmp'];
const MAX_SIZE = 10 * 1024 * 1024; // 10 MB

export default function UploadZone({ onFileSelect }) {
  const [dragOver, setDragOver] = useState(false);
  const inputRef = useRef(null);

  const validateFile = (file) => {
    if (!ACCEPTED_TYPES.includes(file.type)) {
      alert('Please upload a valid image file (JPEG, PNG, WebP, or BMP).');
      return false;
    }
    if (file.size > MAX_SIZE) {
      alert('File size exceeds 10 MB limit.');
      return false;
    }
    return true;
  };

  const handleFile = (file) => {
    if (file && validateFile(file)) {
      onFileSelect(file);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    handleFile(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = () => setDragOver(false);

  const handleChange = (e) => {
    const file = e.target.files[0];
    handleFile(file);
    e.target.value = '';
  };

  return (
    <div
      className={`upload-zone ${dragOver ? 'upload-zone--dragover' : ''}`}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onClick={() => inputRef.current?.click()}
      role="button"
      tabIndex={0}
      aria-label="Upload image"
    >
      <div className="upload-zone__icon">📤</div>
      <div className="upload-zone__title">
        Drag & drop your image here
      </div>
      <div className="upload-zone__subtitle">
        or click to browse — JPEG, PNG, WebP, BMP (max 10 MB)
      </div>
      <input
        ref={inputRef}
        type="file"
        className="upload-zone__input"
        accept={ACCEPTED_TYPES.join(',')}
        onChange={handleChange}
        style={{ display: 'none' }}
      />
    </div>
  );
}

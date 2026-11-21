function formatSize(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

export default function ImagePreview({ file, previewUrl, onRemove }) {
  if (!file || !previewUrl) return null;

  return (
    <div className="image-preview animate-scale-in">
      <img
        src={previewUrl}
        alt="Uploaded preview"
        className="image-preview__img"
      />
      <div className="image-preview__overlay">
        <button
          className="image-preview__remove"
          onClick={onRemove}
          aria-label="Remove image"
          title="Remove image"
        >
          ✕
        </button>
      </div>
      <div className="image-preview__info">
        <span>{file.name}</span>
        <span>{formatSize(file.size)}</span>
      </div>
    </div>
  );
}

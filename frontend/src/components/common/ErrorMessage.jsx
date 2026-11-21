import Button from './Button';

export default function ErrorMessage({ title, message, onRetry }) {
  return (
    <div className="error-card animate-fade-in">
      <div className="error-card__icon">❌</div>
      <div className="error-card__title">{title || 'Something went wrong'}</div>
      <p className="error-card__message">
        {message || 'An unexpected error occurred. Please try again.'}
      </p>
      {onRetry && (
        <Button variant="outline" onClick={onRetry}>
          🔄 Try Again
        </Button>
      )}
    </div>
  );
}

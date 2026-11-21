export default function Loading({ message }) {
  return (
    <div className="loading">
      <div className="loading__spinner" />
      {message && (
        <p className="loading__message">
          {message}<span className="loading__dots" />
        </p>
      )}
    </div>
  );
}

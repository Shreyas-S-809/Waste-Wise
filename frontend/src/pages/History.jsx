import { useState, useEffect } from 'react';
import { getHistory, deleteHistory } from '../api/history';

export default function History() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchRecords = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await getHistory(1);
      const items = response.data?.records || response.records || response.data?.items || [];
      setRecords(items);
    } catch (err) {
      setError(err.message || 'Failed to load audit history.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecords();
  }, []);

  const handleDelete = async (id) => {
    try {
      await deleteHistory(id);
      setRecords((prev) => prev.filter((r) => r.id !== id));
    } catch (err) {
      alert('Failed to delete record: ' + err.message);
    }
  };

  const getBadgeStyle = (cat) => {
    if (cat === 'Wet' || cat === 'Properly Segregated') return 'result-badge--wet';
    if (cat === 'Dry') return 'result-badge--dry';
    return 'result-badge--uncertain';
  };

  return (
    <div className="scroll-pane animate-fade-in">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <div>
          <h2 style={{ fontSize: '19px', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '4px' }}>
            Audit Trail Records
          </h2>
          <p style={{ fontSize: '13.5px', color: 'var(--text-secondary)' }}>
            Historical waste classification inferences stored in local SQLite database
          </p>
        </div>

        <button className="btn-secondary" onClick={fetchRecords} disabled={loading} style={{ padding: '6px 14px', fontSize: '13px' }}>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="23 4 23 10 17 10"></polyline>
            <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path>
          </svg>
          <span>Refresh</span>
        </button>
      </div>

      {error && (
        <div className="alert-box alert-box--warning" style={{ marginBottom: '16px' }}>
          <div>{error}</div>
        </div>
      )}

      {loading ? (
        <div className="card-dark" style={{ textAlign: 'center', padding: '32px' }}>
          <div style={{ color: 'var(--text-muted)', fontSize: '13px' }}>
            Loading audit history records...
          </div>
        </div>
      ) : records.length === 0 ? (
        <div className="card-dark empty-state" style={{ padding: '40px' }}>
          <div className="empty-state__icon">🗂️</div>
          <div className="empty-state__title">No Audit History Found</div>
          <div className="empty-state__description">
            Classifications performed in the workspace will appear here in chronological order.
          </div>
        </div>
      ) : (
        <div className="card-dark" style={{ padding: 0, overflow: 'hidden' }}>
          <table className="history-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Timestamp</th>
                <th>Mode</th>
                <th>Prediction</th>
                <th>Confidence</th>
                <th>Model</th>
                <th style={{ textAlign: 'right' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {records.map((r) => (
                <tr key={r.id}>
                  <td style={{ fontFamily: 'var(--font-mono)' }}>#{r.id}</td>
                  <td>{r.created_at ? new Date(r.created_at).toLocaleString() : 'N/A'}</td>
                  <td>
                    <span style={{ textTransform: 'capitalize' }}>
                      {r.classification_mode || 'item'}
                    </span>
                  </td>
                  <td>
                    <span className={`result-badge ${getBadgeStyle(r.predicted_category)}`}>
                      {r.predicted_category}
                    </span>
                  </td>
                  <td style={{ fontFamily: 'var(--font-mono)' }}>
                    {(r.confidence_score * 100).toFixed(1)}%
                  </td>
                  <td style={{ fontFamily: 'var(--font-mono)', fontSize: '12px' }}>
                    {r.model_name}
                  </td>
                  <td style={{ textAlign: 'right' }}>
                    <button
                      className="btn-secondary"
                      onClick={() => handleDelete(r.id)}
                      style={{ padding: '4px 8px', color: 'var(--accent-red)', fontSize: '12px' }}
                      title="Delete record"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
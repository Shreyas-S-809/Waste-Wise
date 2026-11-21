import { useState, useCallback } from 'react';
import { classifyItem, classifySegregation } from '../api/prediction';

/**
 * Custom hook for managing prediction state.
 * @param {'item'|'segregation'} mode - Classification mode
 * @returns {{ loading, result, error, classify, reset }}
 */
export default function usePrediction(mode) {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const classify = useCallback(async (file) => {
    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('image', file);

    try {
      const classifyFn = mode === 'segregation' ? classifySegregation : classifyItem;
      const data = await classifyFn(formData);
      setResult(data);
      return data;
    } catch (err) {
      const message = err.message || 'Classification failed. Please try again.';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [mode]);

  const reset = useCallback(() => {
    setLoading(false);
    setResult(null);
    setError(null);
  }, []);

  return { loading, result, error, classify, reset };
}

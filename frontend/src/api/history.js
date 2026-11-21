import apiClient from './client';

/**
 * Fetch classification history (paginated).
 * @param {number} page - Page number
 * @returns {Promise<Object>} Paginated history records
 */
export async function getHistory(page = 1) {
  return apiClient.get('/history', { params: { page } });
}

/**
 * Get a single history record by ID.
 * @param {string|number} id
 * @returns {Promise<Object>} History record
 */
export async function getHistoryById(id) {
  return apiClient.get(`/history/${id}`);
}

/**
 * Delete a history record.
 * @param {string|number} id
 * @returns {Promise<Object>}
 */
export async function deleteHistory(id) {
  return apiClient.delete(`/history/${id}`);
}

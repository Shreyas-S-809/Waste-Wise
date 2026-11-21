import apiClient from './client';

/**
 * Classify a single waste item image.
 * @param {FormData} formData - FormData containing the image file under key 'image'
 * @returns {Promise<Object>} Classification result
 */
export async function classifyItem(formData) {
  return apiClient.post('/predict/item', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
}

/**
 * Classify a waste segregation scene.
 * @param {FormData} formData - FormData containing the image file under key 'image'
 * @returns {Promise<Object>} Segregation classification result
 */
export async function classifySegregation(formData) {
  return apiClient.post('/predict/segregation', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
}

/**
 * Get the status of all ML models.
 * @returns {Promise<Object>} Model status info
 */
export async function getModelsStatus() {
  return apiClient.get('/models/status');
}

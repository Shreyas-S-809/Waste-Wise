import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api/v1',
  timeout: 60000,
  headers: {
    'Accept': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => config,
  (error) => Promise.reject(error)
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    let message =
      error.response?.data?.error ||
      error.response?.data?.message;

    if (!message) {
      const responseDataStr = typeof error.response?.data === 'string' ? error.response.data : '';
      if (responseDataStr.includes('ECONNREFUSED') || error.message?.includes('Network Error')) {
        message = 'Cannot connect to WasteWise backend. Please ensure the Flask server is running on port 5000.';
      } else if (error.response?.status === 500) {
        message = 'Backend server unavailable or proxy error (HTTP 500). Please verify the Flask backend is running on port 5000.';
      } else if (error.response?.status === 503) {
        message = 'Model service unavailable (HTTP 503). Model training may still be required.';
      } else {
        message = error.message || 'An unexpected error occurred. Please try again.';
      }
    }

    const status = error.response?.status;

    const enhancedError = new Error(message);
    enhancedError.status = status;
    enhancedError.originalError = error;

    return Promise.reject(enhancedError);
  }
);

export default apiClient;

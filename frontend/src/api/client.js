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
    let message = null;
    const resData = error.response?.data;

    if (typeof resData === 'string') {
      message = resData;
    } else if (resData && typeof resData === 'object') {
      if (typeof resData.error === 'string') {
        message = resData.error;
      } else if (resData.error && typeof resData.error.message === 'string') {
        message = resData.error.message;
      } else if (typeof resData.message === 'string') {
        message = resData.message;
      } else if (typeof resData.error === 'object') {
        message = JSON.stringify(resData.error);
      }
    }

    if (!message) {
      if (error.message?.includes('Network Error') || error.code === 'ERR_NETWORK') {
        message = 'Cannot connect to WasteWise backend. Please ensure the server is running.';
      } else if (error.response?.status === 500) {
        message = 'Backend server error (HTTP 500). Please check server logs.';
      } else if (error.response?.status === 503) {
        message = 'Model service unavailable (HTTP 503). Model training may still be required.';
      } else {
        message = error.message || 'An unexpected error occurred. Please try again.';
      }
    }

    const status = error.response?.status;
    const enhancedError = new Error(String(message));
    enhancedError.status = status;
    enhancedError.originalError = error;

    return Promise.reject(enhancedError);
  }
);

export default apiClient;

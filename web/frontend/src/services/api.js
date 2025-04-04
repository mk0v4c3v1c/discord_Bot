import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  withCredentials: true,
});

// Bot endpoints
export const getBotStatus = () => api.get('/bot/status');
export const restartBot = () => api.post('/bot/restart');

// User endpoints
export const getUsers = (limit = 10) => api.get(`/users?limit=${limit}`);
export const updateUser = (userId, data) => api.patch(`/users/${userId}`, data);

// Stock market
export const getStocks = () => api.get('/stocks');
export const getPortfolio = (userId) => api.get(`/portfolio/${userId}`);

// Error handling
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error);
    throw error;
  }
);
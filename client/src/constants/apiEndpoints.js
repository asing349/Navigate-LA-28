// src/constants/apiEndpoints.js

const API_BASE_URL = "http://localhost:8000/api";

export const AUTH_ENDPOINTS = {
  LOGIN: `${API_BASE_URL}/auth/token/`,
  REGISTER: `${API_BASE_URL}/users/users/`,
};

export const LOCATION_ENDPOINTS = {
  SEARCH: `${API_BASE_URL}/locations/search`,
};

export default API_BASE_URL;

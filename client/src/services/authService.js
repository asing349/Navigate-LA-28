// src/services/authService.js
import axios from "../utils/api";
import { AUTH_ENDPOINTS } from "../constants/apiEndpoints";

/**
 * Authenticate user login.
 * @param {Object} formData - User credentials { username, password }.
 * @returns {Promise} Response from server.
 */
export const loginUser = async (formData) => {
  const response = await axios.post(
    AUTH_ENDPOINTS.LOGIN,
    new URLSearchParams(formData)
  );
  return response.data;
};

/**
 * Register a new user.
 * @param {Object} formData - User details { username, password, dob, country }.
 * @returns {Promise} Response from server.
 */
export const registerUser = async (formData) => {
  const response = await axios.post(AUTH_ENDPOINTS.REGISTER, formData);
  return response.data;
};

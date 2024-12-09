// src/services/mapService.js
import axios from "../utils/api";
import { LOCATION_ENDPOINTS } from "../constants/apiEndpoints";

/**
 * Fetch location data based on query.
 * @param {String} query - Location search query.
 * @returns {Promise} Response from server.
 */
export const fetchLocations = async (query) => {
  const response = await axios.get(`${LOCATION_ENDPOINTS.SEARCH}?q=${query}`);
  return response.data;
};

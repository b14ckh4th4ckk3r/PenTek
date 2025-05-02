import axios from 'axios';

const API_URL = 'http://localhost:5000/api/scan';

export const startScan = async (domain, scanType, mode) => {
  return axios.post(`${API_URL}/start`, { domain, scan_type: scanType, mode });
};

export const getScanStatus = async () => {
  return axios.get(`${API_URL}/status`);
};

export const getScanResults = async () => {
  return axios.get(`${API_URL}/results`);
};

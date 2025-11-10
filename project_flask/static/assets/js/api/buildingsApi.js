import { apiFetch } from '../auth/fetchClient.js';

export function listBuildings(params) { 
  const qs = new URLSearchParams(params || {}).toString();
  return apiFetch('/buildings?' + qs, { method: 'GET' });
}

export function getBuilding(id) { 
  return apiFetch(`/buildings/${id}`, { method: 'GET' }); 
}

export function createBuilding(formData) { 
  // For file uploads, we need to bypass apiFetch's JSON serialization
  // and handle FormData directly with proper authentication
  const getAccessToken = () => {
    try {
      return sessionStorage.getItem('pf_access') || localStorage.getItem('access_token');
    } catch (e) {
      return null;
    }
  };

  const accessToken = getAccessToken();
  const headers = {};
  if (accessToken) {
    headers['Authorization'] = `Bearer ${accessToken}`;
  }

  return fetch('/api/buildings', {
    method: 'POST',
    headers: headers,
    body: formData // FormData should be passed as-is, browser will set Content-Type
  }).then(response => {
    if (!response.ok) {
      return response.json().then(err => Promise.reject(err));
    }
    return response.json();
  });
}

export function deleteBuilding(id) { 
  return apiFetch(`/buildings/${id}`, { method: 'DELETE' }); 
}

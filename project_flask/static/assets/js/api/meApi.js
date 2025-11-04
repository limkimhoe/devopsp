import { apiFetch } from './../auth/fetchClient.js';
export const getMe = ()=> apiFetch('/me', { method:'GET' });
export const patchMe = (data)=> apiFetch('/me', { method:'PATCH', body: data });

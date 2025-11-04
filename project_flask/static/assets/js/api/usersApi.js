import { apiFetch } from '../auth/fetchClient.js';
export function listUsers(params){ 
  const qs = new URLSearchParams(params||{}).toString();
  return apiFetch('/admin/users?'+qs, { method:'GET' });
}
export async function listRoles(){
  // returns array of role names
  return apiFetch('/admin/users/roles', { method: 'GET' });
}
export function getUser(id){ return apiFetch(`/admin/users/${id}`, { method:'GET' }); }
export function createUser(payload){ return apiFetch('/admin/users', { method:'POST', body: payload }); }
export function updateUser(id, payload){ return apiFetch(`/admin/users/${id}`, { method:'PATCH', body: payload }); }
export function banUser(id, reason){ return apiFetch(`/admin/users/${id}/ban`, { method:'POST', body: { reason } }); }
export function unbanUser(id){ return apiFetch(`/admin/users/${id}/unban`, { method:'POST' }); }

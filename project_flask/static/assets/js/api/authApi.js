import { apiFetch } from '../auth/fetchClient.js';
import { setAccessToken, setRefreshToken, clearAll } from '../auth/tokenStore.js';

export async function login(email, password){
  // do NOT pass base: undefined — let apiFetch use configured API_BASE_URL
  const json = await apiFetch('/auth/login', { method:'POST', body: { email, password } });
  if (json.access) setAccessToken(json.access);
  if (json.refresh) setRefreshToken(json.refresh);
  return json;
}
export async function logout(){
  try{ await apiFetch('/auth/logout', { method:'POST' }); }catch(e){}
  clearAll();
  window.location.href = '/login.html';
}
export async function refresh(){
  // handled inside fetchClient
  return apiFetch('/auth/refresh', { method:'POST' });
}

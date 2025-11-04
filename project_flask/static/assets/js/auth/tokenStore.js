/*
 Simple token store:
 - access token in-memory + sessionStorage fallback
 - refresh token handled via cookie (preferred) or localStorage if configured
*/
import { TOKEN_STORAGE_STRATEGY } from '../config.js';
const ACCESS_KEY = 'pf_access';
const REFRESH_KEY = 'pf_refresh_encrypted';

let access = null;
export function setAccessToken(t){
  access = t;
  try{ sessionStorage.setItem(ACCESS_KEY, t); }catch(e){}
}
export function getAccessToken(){
  if (access) return access;
  try{ access = sessionStorage.getItem(ACCESS_KEY); return access; }catch(e){ return null; }
}
export function clearAccessToken(){
  access = null;
  try{ sessionStorage.removeItem(ACCESS_KEY); }catch(e){}
}

export function setRefreshToken(t){
  if (TOKEN_STORAGE_STRATEGY === 'local_encrypted'){
    try{ localStorage.setItem(REFRESH_KEY, t); }catch(e){}
  } else {
    // prefer cookie set by server (HttpOnly). If server returns JSON refresh, we store plain localStorage as fallback.
    try{ localStorage.setItem(REFRESH_KEY, t); }catch(e){}
  }
}
export function getRefreshToken(){
  try{ return localStorage.getItem(REFRESH_KEY); }catch(e){ return null; }
}
export function clearRefreshToken(){
  try{ localStorage.removeItem(REFRESH_KEY); }catch(e){}
}
export function clearAll(){
  clearAccessToken(); clearRefreshToken();
}

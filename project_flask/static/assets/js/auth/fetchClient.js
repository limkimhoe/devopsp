import { API_BASE_URL, REQUEST_ID_HEADER } from '../config.js';
import { getAccessToken, setAccessToken, clearAll, getRefreshToken, setRefreshToken } from './tokenStore.js';
import { toastError } from '../utils/toast.js';

function uuidv4(){ return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c=>{ const r=Math.random()*16|0; const v=c==='x'?r:(r&0x3|0x8); return v.toString(16); }); }

async function rawFetch(url, opts){
  return fetch(url, opts);
}

export async function apiFetch(path, { method='GET', headers={}, body=null, retryOn401=true, base=API_BASE_URL } = {} ){
  const url = path.startsWith('http') ? path : base.replace(/\/+$/,'') + '/'+ path.replace(/^\/+/,'');
  const opts = { method, headers: {...headers, Accept: 'application/json'}, credentials: 'include' };
  if (body && typeof body === 'object'){
    opts.body = JSON.stringify(body);
    opts.headers['Content-Type'] = 'application/json';
  } else if (body){
    opts.body = body;
  }

  const at = getAccessToken();
  if (at) opts.headers['Authorization'] = 'Bearer '+at;
  opts.headers[REQUEST_ID_HEADER] = uuidv4();

  let res = await rawFetch(url, opts);
  if (res.status === 401 && retryOn401){
    // try refresh
    const refreshed = await attemptRefresh();
    if (refreshed){
      // retry once
      const at2 = getAccessToken();
      if (at2) opts.headers['Authorization'] = 'Bearer '+at2;
      res = await rawFetch(url, opts);
    } else {
      // redirect to login
      clearAll();
      toastError('Session expired, please login again');
      window.location.href = '/login.html';
      throw { status: 401, code: 'unauthenticated', message: 'Refresh failed' };
    }
  }

  if (!res.ok){
    let json = null;
    try{ json = await res.json(); }catch(e){}
    const error = { status: res.status, code: json?.code || null, message: json?.detail || res.statusText, details: json };
    if (res.status === 403 && error.code === 'user_banned'){
      clearAll();
      window.location.href = '/403.html';
    }
    throw error;
  }

  const contentType = res.headers.get('content-type') || '';
  if (contentType.includes('application/json')){
    return res.json();
  } else {
    return res.text();
  }
}

let refreshing = false;
let refreshPromise = null;
async function attemptRefresh(){
  if (refreshing && refreshPromise) return refreshPromise;
  refreshing = true;
  refreshPromise = (async ()=>{
    try{
      // call refresh endpoint, backend should set cookie or return JSON
      const r = await rawFetch(API_BASE_URL.replace(/\/+$/,'') + '/auth/refresh', { method: 'POST', credentials: 'include', headers:{ Accept:'application/json' } });
      if (!r.ok) { refreshing=false; return false; }
      const json = await r.json();
      if (json.access) setAccessToken(json.access);
      if (json.refresh) setRefreshToken(json.refresh);
      refreshing = false;
      return true;
    }catch(e){
      refreshing=false;
      return false;
    }
  })();
  return refreshPromise;
}

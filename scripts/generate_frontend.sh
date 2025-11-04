#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FRONTEND="$ROOT/frontend"
mkdir -p "$FRONTEND"
mkdir -p "$FRONTEND/admin"
mkdir -p "$FRONTEND/assets/css"
mkdir -p "$FRONTEND/assets/js/utils"
mkdir -p "$FRONTEND/assets/js/auth"
mkdir -p "$FRONTEND/assets/js/api"
mkdir -p "$FRONTEND/assets/js/pages"
mkdir -p "$FRONTEND/assets/js/components"

cat > "$FRONTEND/login.html" <<'HTML'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Project Flask — Login</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="../assets/css/main.css">
</head>
<body class="bg-light">
  <main class="container py-5">
    <div class="row justify-content-center">
      <div class="col-12 col-md-6 col-lg-4">
        <div class="card shadow-sm">
          <div class="card-body">
            <h3 class="card-title text-center mb-3">Sign in</h3>
            <form id="loginForm" novalidate>
              <div id="alert" class="alert d-none" role="alert"></div>

              <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input id="email" name="email" type="email" class="form-control" required>
                <div class="invalid-feedback">Please enter a valid email.</div>
              </div>

              <div class="mb-3">
                <label for="password" class="form-label d-flex justify-content-between">
                  <span>Password</span>
                  <a href="#" class="small">Forgot?</a>
                </label>
                <div class="input-group">
                  <input id="password" name="password" type="password" class="form-control" required>
                  <button id="togglePwd" type="button" class="btn btn-outline-secondary" aria-label="Show password">Show</button>
                </div>
                <div class="invalid-feedback">Password required.</div>
              </div>

              <div class="d-grid">
                <button id="submitBtn" type="submit" class="btn btn-primary">Login</button>
              </div>
            </form>
          </div>
        </div>

        <p class="text-center text-muted mt-3 small">Demo frontend — no registration. Use admin@example.com / AdminPass123!</p>
      </div>
    </div>
  </main>

  <script type="module" src="../assets/js/pages/login.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
HTML

cat > "$FRONTEND/admin/users.html" <<'HTML'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Admin — Users</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="../assets/css/main.css">
</head>
<body>
  <div id="navbar"></div>
  <main class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h1 class="h4">Users</h1>
      <div>
        <button id="createUserBtn" class="btn btn-sm btn-primary">Create User</button>
      </div>
    </div>

    <div id="filters" class="card mb-3 p-3">
      <!-- filter form (search, role, status, sort, per page) -->
      <form id="filtersForm" class="row g-2 align-items-end">
        <div class="col-md-4">
          <label class="form-label">Search</label>
          <input name="search" class="form-control" placeholder="email or name">
        </div>
        <div class="col-md-2">
          <label class="form-label">Role</label>
          <select name="role" class="form-select">
            <option value="">Any</option>
            <option value="admin">Admin</option>
            <option value="standard">Standard</option>
          </select>
        </div>
        <div class="col-md-2">
          <label class="form-label">Status</label>
          <select name="status" class="form-select">
            <option value="">Any</option>
            <option value="active">Active</option>
            <option value="banned">Banned</option>
          </select>
        </div>
        <div class="col-md-2">
          <label class="form-label">Sort</label>
          <select name="sort" class="form-select">
            <option value="created_at_desc">Created (new)</option>
            <option value="created_at_asc">Created (old)</option>
          </select>
        </div>
        <div class="col-md-2 text-end">
          <button id="applyFilters" class="btn btn-primary">Apply</button>
        </div>
      </form>
    </div>

    <div id="tableWrap" class="table-responsive">
      <table class="table table-sm table-hover">
        <thead class="table-light sticky-top">
          <tr>
            <th>Email</th>
            <th>Roles</th>
            <th>Active</th>
            <th>Banned</th>
            <th>Created</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody id="usersTbody">
          <!-- rows populated by JS -->
        </tbody>
      </table>
    </div>

    <div id="pagination" class="my-3"></div>
  </main>

  <script type="module" src="../assets/js/pages/admin-users.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
HTML

cat > "$FRONTEND/admin/user-detail.html" <<'HTML'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Admin — User</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="../assets/css/main.css">
</head>
<body>
  <div id="navbar"></div>
  <main class="container py-4">
    <a href="users.html" class="btn btn-link">&larr; Back to users</a>
    <div id="detail" class="mt-3"></div>
  </main>

  <script type="module" src="../assets/js/pages/admin-user-detail.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
HTML

cat > "$FRONTEND/me.html" <<'HTML'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>My Profile</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/main.css">
</head>
<body>
  <div id="navbar"></div>
  <main class="container py-4">
    <div class="row">
      <div class="col-md-8">
        <div class="card mb-3">
          <div class="card-body">
            <h5 class="card-title">Profile</h5>
            <form id="meForm">
              <div class="mb-3">
                <label class="form-label">Display name</label>
                <input name="display_name" class="form-control">
              </div>
              <div class="mb-3">
                <label class="form-label">First name</label>
                <input name="first_name" class="form-control">
              </div>
              <div class="mb-3">
                <label class="form-label">Last name</label>
                <input name="last_name" class="form-control">
              </div>
              <div class="mb-3">
                <label class="form-label">Phone</label>
                <input name="phone" class="form-control">
              </div>
              <div class="mb-3">
                <label class="form-label">Avatar URL</label>
                <input name="avatar_url" class="form-control">
              </div>
              <div class="d-grid">
                <button class="btn btn-primary" id="saveBtn">Save</button>
              </div>
            </form>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div id="accountCard" class="card">
          <div class="card-body">
            <h6 class="card-title">Account</h6>
            <p id="accountInfo"></p>
          </div>
        </div>
      </div>
    </div>
  </main>

  <script type="module" src="assets/js/pages/me.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
HTML

cat > "$FRONTEND/403.html" <<'HTML'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>403 Forbidden</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="d-flex align-items-center justify-content-center" style="height:100vh">
  <div class="text-center">
    <h1 class="display-4">403</h1>
    <p class="lead">You are not allowed to view this page.</p>
    <a href="login.html" class="btn btn-primary">Go to Login</a>
  </div>
</body>
</html>
HTML

cat > "$FRONTEND/404.html" <<'HTML'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>404 Not Found</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="d-flex align-items-center justify-content-center" style="height:100vh">
  <div class="text-center">
    <h1 class="display-4">404</h1>
    <p class="lead">The page was not found.</p>
    <a href="index.html" class="btn btn-primary">Back Home</a>
  </div>
</body>
</html>
HTML

cat > "$FRONTEND/assets/css/main.css" <<'CSS'
/* Minimal custom styles */
body { background: #f8f9fa; }
.card { border-radius: .5rem; }
.sticky-top thead { position: sticky; top: 0; z-index: 1; }
.truncate-ellipsis { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.navbar-brand small { font-size: .85rem; opacity: .8; }
CSS

cat > "$FRONTEND/assets/js/config.js" <<'JS'
export const API_BASE_URL = (window.API_BASE_URL || 'http://127.0.0.1:8000/api');
export const TOKEN_STORAGE_STRATEGY = 'cookie'; // 'cookie' or 'local_encrypted'
export const REQUEST_ID_HEADER = 'X-Request-Id';
JS

cat > "$FRONTEND/assets/js/utils/dom.js" <<'JS'
export const $ = (s, root=document) => root.querySelector(s);
export const $$ = (s, root=document) => Array.from(root.querySelectorAll(s));
export const el = (tag, props={}, ...children) => {
  const node = document.createElement(tag);
  Object.entries(props).forEach(([k,v]) => node.setAttribute(k,v));
  children.forEach(c => node.append(typeof c === 'string' ? document.createTextNode(c) : c));
  return node;
};
export const show = (el) => el.classList.remove('d-none');
export const hide = (el) => el.classList.add('d-none');
JS

cat > "$FRONTEND/assets/js/utils/forms.js" <<'JS'
export function serializeForm(form) {
  const data = {};
  new FormData(form).forEach((v,k) => {
    data[k] = v;
  });
  return data;
}
export function setFormValues(form, data) {
  Object.entries(data).forEach(([k,v])=>{
    const input = form.elements[k];
    if (!input) return;
    input.value = v ?? '';
  });
}
export function validateEmail(v){ return /\S+@\S+\.\S+/.test(v); }
export function validateURL(v){ try{ new URL(v); return true }catch(e){ return false } }
JS

cat > "$FRONTEND/assets/js/utils/toast.js" <<'JS'
export function toastSuccess(msg){ toast(msg, 'success'); }
export function toastError(msg){ toast(msg, 'danger'); }
export function toastInfo(msg){ toast(msg, 'info'); }
function toast(msg, type='info'){
  const containerId = 'toastRoot';
  let root = document.getElementById(containerId);
  if (!root){
    root = document.createElement('div');
    root.id = containerId;
    root.style.position = 'fixed';
    root.style.right = '1rem';
    root.style.top = '1rem';
    root.style.zIndex = 1050;
    document.body.appendChild(root);
  }
  const el = document.createElement('div');
  el.className = `toast align-items-center text-bg-${type} border-0 show`;
  el.setAttribute('role','alert');
  el.style.minWidth = '200px';
  el.innerHTML = `<div class="d-flex">
    <div class="toast-body">${msg}</div>
    <button type="button" class="btn-close btn-close-white me-2 m-auto" aria-label="Close"></button>
  </div>`;
  root.appendChild(el);
  el.querySelector('button').onclick = ()=> el.remove();
  setTimeout(()=> el.remove(), 5000);
}
JS

cat > "$FRONTEND/assets/js/auth/tokenStore.js" <<'JS'
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
JS

cat > "$FRONTEND/assets/js/auth/fetchClient.js" <<'JS'
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
JS

cat > "$FRONTEND/assets/js/api/authApi.js" <<'JS'
import { apiFetch } from '../auth/fetchClient.js';
import { setAccessToken, setRefreshToken, clearAll } from '../auth/tokenStore.js';

export async function login(email, password){
  const json = await apiFetch('/auth/login', { method:'POST', body: { email, password } , base:undefined });
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
JS

cat > "$FRONTEND/assets/js/api/meApi.js" <<'JS'
import { apiFetch } from './../auth/fetchClient.js';
export const getMe = ()=> apiFetch('/me', { method:'GET' });
export const patchMe = (data)=> apiFetch('/me', { method:'PATCH', body: data });
JS

cat > "$FRONTEND/assets/js/api/usersApi.js" <<'JS'
import { apiFetch } from '../auth/fetchClient.js';
export function listUsers(params){ 
  const qs = new URLSearchParams(params||{}).toString();
  return apiFetch('/admin/users?'+qs, { method:'GET' });
}
export function getUser(id){ return apiFetch(`/admin/users/${id}`, { method:'GET' }); }
export function createUser(payload){ return apiFetch('/admin/users', { method:'POST', body: payload }); }
export function updateUser(id, payload){ return apiFetch(`/admin/users/${id}`, { method:'PATCH', body: payload }); }
export function banUser(id, reason){ return apiFetch(`/admin/users/${id}/ban`, { method:'POST', body: { reason } }); }
export function unbanUser(id){ return apiFetch(`/admin/users/${id}/unban`, { method:'POST' }); }
JS

cat > "$FRONTEND/assets/js/components/navbar.js" <<'JS'
import { getMe } from '../api/meApi.js';
import { apiFetch } from '../auth/fetchClient.js';
export async function renderNavbar(containerId='navbar'){
  const el = document.getElementById(containerId);
  try{
    const me = await apiFetch('/me', { method: 'GET' });
    const roles = me.roles||[];
    const email = me.email;
    el.innerHTML = `
<nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom">
  <div class="container">
    <a class="navbar-brand" href="/"><strong>ProjectFlask</strong> <small>demo</small></a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMain">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navMain">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        ${roles.includes('admin') ? '<li class="nav-item"><a class="nav-link" href="/admin/users.html">Users</a></li>' : ''}
        <li class="nav-item"><a class="nav-link" href="/me.html">My Profile</a></li>
      </ul>
      <div class="d-flex align-items-center">
        <span class="me-3 small text-muted">${email}</span>
        <a id="logoutBtn" class="btn btn-outline-secondary btn-sm" href="#">Logout</a>
      </div>
    </div>
  </div>
</nav>`;
    document.getElementById('logoutBtn').addEventListener('click', async (e)=>{
      e.preventDefault();
      await apiFetch('/auth/logout', { method:'POST' });
      window.location.href='/login.html';
    });
  }catch(e){
    el.innerHTML = '';
  }
}
renderNavbar();
JS

cat > "$FRONTEND/assets/js/pages/login.js" <<'JS'
import { login } from '../api/authApi.js';
import { validateEmail } from '../utils/forms.js';
const form = document.getElementById('loginForm');
const alertEl = document.getElementById('alert');
const pwdToggle = document.getElementById('togglePwd');

pwdToggle.addEventListener('click', ()=> {
  const pwd = document.getElementById('password');
  pwd.type = pwd.type === 'password' ? 'text' : 'password';
  pwdToggle.textContent = pwd.type === 'password' ? 'Show' : 'Hide';
});

form.addEventListener('submit', async (e)=>{
  e.preventDefault();
  alertEl.classList.add('d-none');
  const email = form.email.value.trim();
  const password = form.password.value;
  if (!validateEmail(email)){ alertEl.className='alert alert-danger'; alertEl.textContent='Invalid email'; alertEl.classList.remove('d-none'); return; }
  if (!password){ alertEl.className='alert alert-danger'; alertEl.textContent='Password required'; alertEl.classList.remove('d-none'); return; }
  try{
    const res = await login(email, password);
    // after login, call /me to determine role & redirect
    const me = await (await fetch((window.API_BASE_URL||'http://127.0.0.1:8000/api').replace(/\/$/,'') + '/me', { credentials:'include' })).json();
    if ((me.roles||[]).includes('admin')) location.href = '/admin/users.html';
    else location.href = '/me.html';
  }catch(err){
    alertEl.className='alert alert-danger';
    alertEl.textContent = err?.message || 'Login failed';
    alertEl.classList.remove('d-none');
  }
});
JS

cat > "$FRONTEND/assets/js/pages/admin-users.js" <<'JS'
import { listUsers } from '../api/usersApi.js';
import { renderNavbar } from '../components/navbar.js';
const tbody = document.getElementById('usersTbody');
const pagination = document.getElementById('pagination');

async function load(page=1){
  tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4">Loading…</td></tr>';
  try{
    const data = await listUsers({ page, per_page: 10 });
    tbody.innerHTML = '';
    data.items.forEach(u=>{
      const tr = document.createElement('tr');
      tr.innerHTML = `<td class="truncate-ellipsis">${u.email}</td>
        <td>${u.roles.join(',')}</td>
        <td>${u.is_active ? 'Yes' : 'No'}</td>
        <td>${u.is_banned ? 'Yes' : 'No'}</td>
        <td>${new Date(u.created_at).toLocaleString()}</td>
        <td>
          <a class="btn btn-sm btn-outline-primary" href="/admin/user-detail.html?id=${u.id}">View</a>
        </td>`;
      tbody.appendChild(tr);
    });
    // simple pagination
    pagination.innerHTML = data.total_pages ? `<nav><ul class="pagination"><li class="page-item"><a class="page-link" href="#" data-page="1">1</a></li>
      <li class="page-item"><a class="page-link" href="#" data-page="${Math.min(2, data.total_pages)}">2</a></li></ul></nav>` : '';
    pagination.querySelectorAll('a[data-page]').forEach(a=>{
      a.addEventListener('click', (e)=>{ e.preventDefault(); load(parseInt(a.dataset.page)); });
    });
  }catch(e){
    tbody.innerHTML = `<tr><td colspan="6" class="text-center text-danger">Failed to load users</td></tr>`;
  }
}

await renderNavbar();
load();
JS

cat > "$FRONTEND/assets/js/pages/admin-user-detail.js" <<'JS'
import { getUser } from '../api/usersApi.js';
import { renderNavbar } from '../components/navbar.js';
const detail = document.getElementById('detail');
const params = new URLSearchParams(location.search);
const id = params.get('id');

async function show(){
  detail.innerHTML = '<div class="text-center py-4">Loading…</div>';
  try{
    const u = await getUser(id);
    detail.innerHTML = `<div class="card">
      <div class="card-body">
        <h5>${u.email} <small class="text-muted">${u.roles.join(',')}</small></h5>
        <p>Active: ${u.is_active}</p>
        <p>Banned: ${u.is_banned} ${u.banned_reason ? '- '+u.banned_reason : ''}</p>
        <p>Created: ${u.created_at}</p>
        <a class="btn btn-primary" href="/admin/users.html">Back</a>
      </div>
    </div>`;
  }catch(e){
    detail.innerHTML = `<div class="alert alert-danger">Failed to load user</div>`;
  }
}

await renderNavbar();
show();
JS

cat > "$FRONTEND/assets/js/pages/me.js" <<'JS'
import { getMe, patchMe } from '../api/meApi.js';
import { renderNavbar } from '../components/navbar.js';
const form = document.getElementById('meForm');
const account = document.getElementById('accountInfo');

async function init(){
  await renderNavbar();
  try{
    const me = await getMe();
    account.innerHTML = `<div><strong>${me.email}</strong><br>${(me.roles||[]).join(', ')}</div>`;
    // set form values
    Object.entries(me.profile||{}).forEach(([k,v])=>{
      const el = form.elements[k];
      if (el) el.value = v ?? '';
    });
  }catch(e){
    window.location.href = '/login.html';
  }
}
form.addEventListener('submit', async (e)=>{
  e.preventDefault();
  const data = {};
  new FormData(form).forEach((v,k)=> data[k]=v);
  try{
    await patchMe(data);
    alert('Saved');
  }catch(e){
    alert('Save failed');
  }
});
init();
JS

cat > "$FRONTEND/assets/js/components/pagination.js" <<'JS'
export function renderPagination(container, { page, per_page, total_pages }, onChange){
  const el = document.getElementById(container);
  if (!el) return;
  el.innerHTML = '';
  const nav = document.createElement('nav');
  const ul = document.createElement('ul');
  ul.className = 'pagination';
  for (let p=1;p<=Math.min(total_pages,10);p++){
    const li = document.createElement('li');
    li.className = 'page-item' + (p===page? ' active':'');
    const a = document.createElement('a');
    a.className = 'page-link';
    a.href='#';
    a.textContent = p;
    a.addEventListener('click', (e)=>{ e.preventDefault(); onChange(p); });
    li.appendChild(a);
    ul.appendChild(li);
  }
  nav.appendChild(ul);
  el.appendChild(nav);
}
JS

cat > "$FRONTEND/README.md" <<'MD'
Frontend static files (no build)
- Open frontend/index.html to auto-route based on authentication.
- For local dev, run a static server (e.g. `python -m http.server` in the frontend/ dir).
- The frontend expects backend API at http://127.0.0.1:8000/api — adjust `assets/js/config.js` if needed.
MD
MD

chmod +x "$FRONTEND" || true
echo "Wrote frontend files to $FRONTEND"

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

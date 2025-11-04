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

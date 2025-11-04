import { getUser, updateUser, listRoles } from '../api/usersApi.js';
import { renderNavbar } from '../components/navbar.js';
import { toastSuccess, toastError } from '../utils/toast.js';

const detail = document.getElementById('detail');
const params = new URLSearchParams(location.search);
const id = params.get('id');
const isEdit = params.get('edit') === '1' || params.get('edit') === 'true';

async function renderView(u){
  detail.innerHTML = `<div class="card">
    <div class="card-body">
      <h5>${u.email} <small class="text-muted">${(u.roles||[]).join(',')}</small></h5>
      <p>Active: ${u.is_active}</p>
      <p>Banned: ${u.is_banned} ${u.banned_reason ? '- '+u.banned_reason : ''}</p>
      <p>Created: ${u.created_at}</p>
      <a class="btn btn-secondary" href="/admin/users.html">&larr; Back</a>
      <a class="btn btn-primary ms-2" href="/admin/user-detail.html?id=${u.id}&edit=1">Edit</a>
    </div>
  </div>`;
}

async function renderEdit(u){
  detail.innerHTML = '<div class="text-center py-4">Loading…</div>';
  let roles = [];
  try { roles = await listRoles(); } catch (e) { roles = []; }
  const roleOptions = roles.map(r => `<option value="${r}" ${((u.roles||[]).includes(r)) ? 'selected' : ''}>${r}</option>`).join('');
  detail.innerHTML = `<form id="editForm" class="card">
    <div class="card-body">
      <h5>Edit user: ${u.email}</h5>
      <div class="mb-3">
        <label class="form-label">Email</label>
        <input name="email" class="form-control" value="${u.email}" disabled>
      </div>
      <div class="mb-3">
        <label class="form-label">Roles</label>
        <select name="roles" multiple class="form-select" style="min-height:120px">
          ${roleOptions}
        </select>
      </div>
      <div class="mb-3 form-check">
        <input type="checkbox" name="is_active" class="form-check-input" id="isActiveChk" ${u.is_active ? 'checked' : ''}>
        <label class="form-check-label" for="isActiveChk">Active</label>
      </div>
      <div class="d-flex">
        <button type="submit" class="btn btn-primary me-2">Save</button>
        <a class="btn btn-secondary" href="/admin/user-detail.html?id=${u.id}">Cancel</a>
      </div>
    </div>
  </form>`;

  const form = document.getElementById('editForm');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const rolesSelected = Array.from(form.querySelector('[name="roles"]').selectedOptions).map(o => o.value);
    const is_active = !!form.querySelector('[name="is_active"]').checked;
    const payload = { roles: rolesSelected, is_active };
    try {
      await updateUser(id, payload);
      toastSuccess('User updated');
      window.location.href = '/admin/users.html';
    } catch (err) {
      console.error('Update failed', err);
      toastError(err?.message || 'Failed to update user');
    }
  });
}

async function show(){
  detail.innerHTML = '<div class="text-center py-4">Loading…</div>';
  try{
    const u = await getUser(id);
    if (isEdit) await renderEdit(u);
    else await renderView(u);
  }catch(e){
    detail.innerHTML = `<div class="alert alert-danger">Failed to load user</div>`;
  }
}

await renderNavbar();
show();

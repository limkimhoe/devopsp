import { listUsers, createUser } from '../api/usersApi.js';
import { apiFetch } from '../auth/fetchClient.js';
import { renderNavbar } from '../components/navbar.js';
import { toastSuccess, toastError } from '../utils/toast.js';

const tbody = document.getElementById('usersTbody');
const pagination = document.getElementById('pagination');
const createBtn = document.getElementById('createUserBtn');

let currentPage = 1;

async function load(page = 1) {
  currentPage = page;
  const perPage = parseInt(document.getElementById('perPageSelect')?.value || 10);
  // gather filter params from form
  const params = { page, per_page: perPage };
  try {
    const filtersForm = document.getElementById('filtersForm');
    if (filtersForm) {
      const fd = new FormData(filtersForm);
      const search = (fd.get('search') || '').trim();
      const role = (fd.get('role') || '').trim();
      const status = (fd.get('status') || '').trim();
      const sort = (fd.get('sort') || '').trim();
      if (search) params.search = search;
      if (role) params.role = role;
      if (status === 'active') params.is_active = true;
      if (status === 'banned') params.is_banned = true;
      if (sort) params.sort = sort;
    }
  } catch (e) {
    // ignore filter parsing errors
  }

  tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4">Loading…</td></tr>';
  try {
    const data = await listUsers(params);
    tbody.innerHTML = '';
    if (!data || !Array.isArray(data.items)) {
      tbody.innerHTML = `<tr><td colspan="6" class="text-center text-muted">No users</td></tr>`;
      pagination.innerHTML = '';
      return;
    }
    data.items.forEach(u => {
      const tr = document.createElement('tr');
      tr.innerHTML = `<td class="truncate-ellipsis">${u.email}</td>
        <td>${(u.roles||[]).join(',')}</td>
        <td>${u.is_active ? 'Yes' : 'No'}</td>
        <td>${u.is_banned ? 'Yes' : 'No'}</td>
        <td>${new Date(u.created_at).toLocaleString()}</td>
        <td>
          <a class="btn btn-sm btn-outline-secondary me-1" href="/admin/user-detail.html?id=${u.id}">View</a>
          <a class="btn btn-sm btn-outline-primary me-1" href="/admin/user-detail.html?id=${u.id}&edit=1">Edit</a>
          <button class="btn btn-sm btn-outline-danger btn-deactivate" data-id="${u.id}" data-active="${u.is_active ? '1' : '0'}" title="${u.is_active ? 'Deactivate' : 'Activate'}">${u.is_active ? 'X' : '✓'}</button>
        </td>`;
      tbody.appendChild(tr);
    });

    // attach handlers for deactivate buttons
    tbody.querySelectorAll('.btn-deactivate').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        e.preventDefault();
        const id = btn.dataset.id;
        const currentlyActive = btn.dataset.active === '1';
        try {
          await (await import('../api/usersApi.js')).updateUser(id, { is_active: !currentlyActive });
          toastSuccess(currentlyActive ? 'User deactivated' : 'User activated');
          load(currentPage);
        } catch (err) {
          console.error('Toggle active failed', err);
          toastError(err.message || 'Failed to update user');
        }
      });
    });

    // build pagination using total_pages (if available) - render with prev/next and numeric pages
    if (data.total_pages && data.total_pages > 1) {
      // debug: ensure pagination rendering runs in browser (will appear in console)
      try { console.log("pagination: total_pages=", data.total_pages, "page=", page); } catch(_) {}
      const totalPages = data.total_pages;
      const currentPageNum = page;

      function pageItem(p, label = null, disabled = false, active = false){
        const lab = label === null ? String(p) : label;
        const cls = 'page-item' + (active ? ' active' : '') + (disabled ? ' disabled' : '');
        return `<li class="${cls}"><a class="page-link" href="#" data-page="${p}">${lab}</a></li>`;
      }

      let html = '<nav aria-label="Page navigation"><ul class="pagination justify-content-center">';

      // prev
      if (currentPageNum > 1) html += pageItem(currentPageNum - 1, '‹', false, false);
      else html += `<li class="page-item disabled"><span class="page-link">‹</span></li>`;

      // show window of pages around current
      const windowSize = 5;
      let start = Math.max(1, currentPageNum - 2);
      let end = Math.min(totalPages, currentPageNum + 2);
      // expand window if near edges
      if (currentPageNum <= 3) { start = 1; end = Math.min(totalPages, windowSize); }
      if (currentPageNum >= totalPages - 2) { end = totalPages; start = Math.max(1, totalPages - windowSize + 1); }

      if (start > 1) {
        html += pageItem(1, '1', false, currentPageNum === 1);
        if (start > 2) html += `<li class="page-item disabled"><span class="page-link">…</span></li>`;
      }

      for (let p = start; p <= end; p++) {
        html += pageItem(p, null, false, p === currentPageNum);
      }

      if (end < totalPages) {
        if (end < totalPages - 1) html += `<li class="page-item disabled"><span class="page-link">…</span></li>`;
        html += pageItem(totalPages, String(totalPages), false, currentPageNum === totalPages);
      }

      // next
      if (currentPageNum < totalPages) html += pageItem(currentPageNum + 1, '›', false, false);
      else html += `<li class="page-item disabled"><span class="page-link">›</span></li>`;

      html += '</ul></nav>';
      pagination.innerHTML = html;

      pagination.querySelectorAll('a[data-page]').forEach(a => {
        a.addEventListener('click', (e) => { e.preventDefault(); const np = parseInt(a.dataset.page); if (!isNaN(np)) load(np); });
      });
    } else {
      pagination.innerHTML = '';
    }
  } catch (e) {
    console.error('Failed to load users', e);
    tbody.innerHTML = `<tr><td colspan="6" class="text-center text-danger">Failed to load users</td></tr>`;
    pagination.innerHTML = '';
  }
}

// Create user modal handling
function setupCreateModal() {
  const modalEl = document.getElementById('createUserModal');
  const form = document.getElementById('createUserForm');
  if (!modalEl || !form) return;

  const bsModal = new bootstrap.Modal(modalEl);

  createBtn.addEventListener('click', async (e) => {
    e.preventDefault();
    form.reset();
    // clear previous errors
    form.querySelectorAll('.is-invalid').forEach(i => i.classList.remove('is-invalid'));

    // populate roles select from server
    const rolesSelect = document.getElementById('createUserRolesSelect');
    if (rolesSelect) {
      rolesSelect.innerHTML = '<option>Loading…</option>';
      try {
        const roles = await (await import('../api/usersApi.js')).listRoles();
        rolesSelect.innerHTML = '';
        roles.forEach(r => {
          const opt = document.createElement('option');
          opt.value = r;
          opt.textContent = r;
          rolesSelect.appendChild(opt);
        });
      } catch (err) {
        rolesSelect.innerHTML = '<option value="">(failed to load roles)</option>';
      }
    }

    bsModal.show();
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    // gather form values
    const fd = new FormData(form);
    const email = (fd.get('email') || '').trim();
    const temp_password = (fd.get('temp_password') || '').trim();
    // read selected roles from multi-select
    const rolesEl = form.querySelector('#createUserRolesSelect');
    const roles = rolesEl ? Array.from(rolesEl.selectedOptions).map(o => o.value) : [];
    const display_name = (fd.get('display_name') || '').trim();

    // basic client validation
    if (!email) {
      form.querySelector('[name="email"]').classList.add('is-invalid');
      return;
    }

    const payload = {
      email,
      temp_password: temp_password || undefined,
      roles: roles,
      profile: display_name ? { display_name } : undefined
    };

    try {
      const res = await createUser(payload);
      toastSuccess('User created');
      bsModal.hide();
      // reload current page
      load(currentPage);
    } catch (err) {
      console.error('Create user failed', err);
      toastError(err.message || 'Failed to create user');
      // if validation details available, mark fields (best-effort)
      const details = err.details || {};
      if (details.errors && typeof details.errors === 'object') {
        Object.keys(details.errors).forEach(k => {
          const el = form.querySelector(`[name="${k}"]`);
          if (el) el.classList.add('is-invalid');
        });
      }
    }
  });
}

function setupFilters(){
  const form = document.getElementById('filtersForm');
  const perSelect = document.getElementById('perPageSelect');
  const applyBtn = document.getElementById('applyFilters');

  // Apply button should trigger a reload when present
  if (applyBtn && form){
    applyBtn.addEventListener('click', (e)=>{
      e.preventDefault();
      load(1);
    });
  }

  // Always attach listener to per-page select so changing rows-per-page
  // immediately reloads the listing and rebuilds the pagination.
  if (perSelect){
    perSelect.addEventListener('change', ()=> {
      load(1);
    });
  }
}

async function ensureAuthenticated(){
  try{
    // quick check - apiFetch will attempt a refresh if needed
    await apiFetch('/me', { method: 'GET' });
    return true;
  }catch(e){
    // not authenticated -> redirect to login
    try{ localStorage.removeItem('pf_refresh_encrypted'); sessionStorage.removeItem('pf_access'); }catch(_){}
    window.location.href = '/login.html';
    throw e;
  }
}

await ensureAuthenticated();
await renderNavbar();
setupCreateModal();
setupFilters();
load();

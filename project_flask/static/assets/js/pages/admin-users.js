import { listUsers, createUser } from '../api/usersApi.js';
import { renderNavbar } from '../components/navbar.js';
import { toastSuccess, toastError } from '../utils/toast.js';

const tbody = document.getElementById('usersTbody');
const pagination = document.getElementById('pagination');
const createBtn = document.getElementById('createUserBtn');

let currentPage = 1;

async function load(page = 1) {
  currentPage = page;
  tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4">Loading…</td></tr>';
  try {
    const data = await listUsers({ page, per_page: 10 });
    tbody.innerHTML = '';
    data.items.forEach(u => {
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

    // build pagination using total_pages (if available)
    if (data.total_pages && data.total_pages > 1) {
      let html = '<nav><ul class="pagination">';
      for (let p = 1; p <= Math.min(7, data.total_pages); p++) {
        const active = p === page ? ' active' : '';
        html += `<li class="page-item${active}"><a class="page-link" href="#" data-page="${p}">${p}</a></li>`;
      }
      if (data.total_pages > 7) {
        html += `<li class="page-item disabled"><span class="page-link">…</span></li>
                 <li class="page-item"><a class="page-link" href="#" data-page="${data.total_pages}">${data.total_pages}</a></li>`;
      }
      html += '</ul></nav>';
      pagination.innerHTML = html;
      pagination.querySelectorAll('a[data-page]').forEach(a => {
        a.addEventListener('click', (e) => { e.preventDefault(); load(parseInt(a.dataset.page)); });
      });
    } else {
      pagination.innerHTML = '';
    }
  } catch (e) {
    console.error('Failed to load users', e);
    tbody.innerHTML = `<tr><td colspan="6" class="text-center text-danger">Failed to load users</td></tr>`;
  }
}

// Create user modal handling
function setupCreateModal() {
  const modalEl = document.getElementById('createUserModal');
  const form = document.getElementById('createUserForm');
  if (!modalEl || !form) return;

  const bsModal = new bootstrap.Modal(modalEl);

  createBtn.addEventListener('click', (e) => {
    e.preventDefault();
    form.reset();
    // clear previous errors
    form.querySelectorAll('.is-invalid').forEach(i => i.classList.remove('is-invalid'));
    bsModal.show();
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    // gather form values
    const fd = new FormData(form);
    const email = (fd.get('email') || '').trim();
    const temp_password = (fd.get('temp_password') || '').trim();
    const rolesRaw = (fd.get('roles') || '').trim();
    const display_name = (fd.get('display_name') || '').trim();

    // basic client validation
    if (!email) {
      form.querySelector('[name="email"]').classList.add('is-invalid');
      return;
    }

    const payload = {
      email,
      temp_password: temp_password || undefined,
      roles: rolesRaw ? rolesRaw.split(',').map(r => r.trim()).filter(Boolean) : [],
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

await renderNavbar();
setupCreateModal();
load();

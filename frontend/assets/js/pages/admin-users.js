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

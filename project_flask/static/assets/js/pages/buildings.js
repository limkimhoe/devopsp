import { listBuildings, createBuilding, getBuilding, deleteBuilding } from '../api/buildingsApi.js';
import { apiFetch } from '../auth/fetchClient.js';
import { renderNavbar } from '../components/navbar.js';
import { toastSuccess, toastError } from '../utils/toast.js';

const tbody = document.getElementById('buildingsTbody');
const pagination = document.getElementById('pagination');
const createBtn = document.getElementById('createBuildingBtn');

let currentPage = 1;

async function load(page = 1) {
  currentPage = page;
  const perPage = parseInt(document.getElementById('perPageSelect')?.value || 10);
  
  // Gather filter params from form
  const params = { page, per_page: perPage };
  try {
    const filtersForm = document.getElementById('filtersForm');
    if (filtersForm) {
      const fd = new FormData(filtersForm);
      const search = (fd.get('search') || '').trim();
      const sort = (fd.get('sort') || '').trim();
      if (search) params.search = search;
      if (sort) params.sort = sort;
    }
  } catch (e) {
    // ignore filter parsing errors
  }

  tbody.innerHTML = '<tr><td colspan="5" class="text-center py-4">Loading…</td></tr>';
  
  try {
    const data = await listBuildings(params);
    tbody.innerHTML = '';
    
    if (!data || !Array.isArray(data.items)) {
      tbody.innerHTML = `<tr><td colspan="5" class="text-center text-muted">No buildings found</td></tr>`;
      pagination.innerHTML = '';
      return;
    }
    
    data.items.forEach(building => {
      const tr = document.createElement('tr');
      const gmlFileName = building.gml_file_path.split('/').pop() || 'N/A';
      const textureFileName = building.texture_file_path.split('/').pop() || 'N/A';
      const createdDate = new Date(building.created_at).toLocaleString();
      
      tr.innerHTML = `
        <td class="truncate-ellipsis">${building.name}</td>
        <td><small>${gmlFileName}</small></td>
        <td><small>${textureFileName}</small></td>
        <td>${createdDate}</td>
        <td>
          <button class="btn btn-sm btn-outline-info me-1 btn-view" data-id="${building.id}" title="View Details">View</button>
          <button class="btn btn-sm btn-outline-danger btn-delete" data-id="${building.id}" title="Delete Building">Delete</button>
        </td>
      `;
      tbody.appendChild(tr);
    });

    // Attach handlers for view and delete buttons
    tbody.querySelectorAll('.btn-view').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        e.preventDefault();
        const id = btn.dataset.id;
        await showBuildingDetails(id);
      });
    });

    tbody.querySelectorAll('.btn-delete').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        e.preventDefault();
        const id = btn.dataset.id;
        if (confirm('Are you sure you want to delete this building? This action cannot be undone.')) {
          try {
            await deleteBuilding(id);
            toastSuccess('Building deleted successfully');
            load(currentPage);
          } catch (err) {
            console.error('Delete building failed', err);
            toastError(err.message || 'Failed to delete building');
          }
        }
      });
    });

    // Build pagination
    if (data.total_pages && data.total_pages > 1) {
      const totalPages = data.total_pages;
      const currentPageNum = page;

      function pageItem(p, label = null, disabled = false, active = false) {
        const lab = label === null ? String(p) : label;
        const cls = 'page-item' + (active ? ' active' : '') + (disabled ? ' disabled' : '');
        return `<li class="${cls}"><a class="page-link" href="#" data-page="${p}">${lab}</a></li>`;
      }

      let html = '<nav aria-label="Page navigation"><ul class="pagination justify-content-center">';

      // Previous
      if (currentPageNum > 1) html += pageItem(currentPageNum - 1, '‹', false, false);
      else html += `<li class="page-item disabled"><span class="page-link">‹</span></li>`;

      // Show window of pages around current
      const windowSize = 5;
      let start = Math.max(1, currentPageNum - 2);
      let end = Math.min(totalPages, currentPageNum + 2);

      // Expand window if near edges
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

      // Next
      if (currentPageNum < totalPages) html += pageItem(currentPageNum + 1, '›', false, false);
      else html += `<li class="page-item disabled"><span class="page-link">›</span></li>`;

      html += '</ul></nav>';
      pagination.innerHTML = html;

      pagination.querySelectorAll('a[data-page]').forEach(a => {
        a.addEventListener('click', (e) => {
          e.preventDefault();
          const np = parseInt(a.dataset.page);
          if (!isNaN(np)) load(np);
        });
      });
    } else {
      pagination.innerHTML = '';
    }
  } catch (e) {
    console.error('Failed to load buildings', e);
    tbody.innerHTML = `<tr><td colspan="5" class="text-center text-danger">Failed to load buildings</td></tr>`;
    pagination.innerHTML = '';
  }
}

// Create building modal handling
function setupCreateModal() {
  const modalEl = document.getElementById('createBuildingModal');
  const form = document.getElementById('createBuildingForm');
  if (!modalEl || !form) return;

  const bsModal = new bootstrap.Modal(modalEl);

  createBtn.addEventListener('click', (e) => {
    e.preventDefault();
    form.reset();
    // Clear previous errors
    form.querySelectorAll('.is-invalid').forEach(i => i.classList.remove('is-invalid'));
    bsModal.show();
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Gather form data
    const formData = new FormData(form);
    const name = (formData.get('name') || '').trim();
    const gmlFile = formData.get('gml_file');
    const textureFile = formData.get('texture_file');

    // Basic client validation
    let isValid = true;
    
    if (!name) {
      form.querySelector('[name="name"]').classList.add('is-invalid');
      isValid = false;
    }
    
    if (!gmlFile || gmlFile.size === 0) {
      form.querySelector('[name="gml_file"]').classList.add('is-invalid');
      isValid = false;
    }
    
    if (!textureFile || textureFile.size === 0) {
      form.querySelector('[name="texture_file"]').classList.add('is-invalid');
      isValid = false;
    }

    if (!isValid) {
      toastError('Please fill in all required fields');
      return;
    }

    try {
      // Show loading state
      const submitBtn = form.querySelector('[type="submit"]');
      const originalText = submitBtn.textContent;
      submitBtn.textContent = 'Uploading...';
      submitBtn.disabled = true;

      const result = await createBuilding(formData);
      toastSuccess('Building uploaded successfully');
      bsModal.hide();
      // Reload current page
      load(currentPage);
    } catch (err) {
      console.error('Create building failed', err);
      toastError(err.detail || err.message || 'Failed to upload building');
    } finally {
      // Reset button state
      const submitBtn = form.querySelector('[type="submit"]');
      submitBtn.textContent = 'Upload';
      submitBtn.disabled = false;
    }
  });
}

// View building details modal
async function showBuildingDetails(buildingId) {
  const modalEl = document.getElementById('viewBuildingModal');
  if (!modalEl) return;

  const bsModal = new bootstrap.Modal(modalEl);
  
  try {
    const building = await getBuilding(buildingId);
    
    // Populate modal with building data
    document.getElementById('viewBuildingName').textContent = building.name;
    document.getElementById('viewBuildingCreated').textContent = new Date(building.created_at).toLocaleString();
    document.getElementById('viewBuildingGmlFile').textContent = building.gml_file_path.split('/').pop();
    document.getElementById('viewBuildingTextureFile').textContent = building.texture_file_path.split('/').pop();
    
    // Load texture image
    loadTextureImage(buildingId);
    
    // Format XML data for display
    const xmlData = building.xml_data;
    let formattedXml = xmlData;
    try {
      // Try to format the XML nicely
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(xmlData, 'text/xml');
      const serializer = new XMLSerializer();
      formattedXml = serializer.serializeToString(xmlDoc);
      
      // Basic indentation (simple approach)
      formattedXml = formattedXml.replace(/></g, '>\n<');
    } catch (e) {
      // If formatting fails, use original
      formattedXml = xmlData;
    }
    
    document.getElementById('viewBuildingXmlData').textContent = formattedXml;
    
    bsModal.show();
  } catch (err) {
    console.error('Failed to load building details', err);
    toastError('Failed to load building details');
  }
}

// Load texture image for building details modal
function loadTextureImage(buildingId) {
  const imageEl = document.getElementById('viewBuildingTextureImage');
  const errorEl = document.getElementById('viewBuildingTextureError');
  const loadingEl = document.getElementById('viewBuildingTextureLoading');
  
  // Reset states
  imageEl.style.display = 'none';
  errorEl.style.display = 'none';
  loadingEl.style.display = 'block';
  
  // Get access token for authenticated request
  const getAccessToken = () => {
    try {
      return sessionStorage.getItem('pf_access') || localStorage.getItem('access_token');
    } catch (e) {
      return null;
    }
  };

  const accessToken = getAccessToken();
  const headers = {};
  if (accessToken) {
    headers['Authorization'] = `Bearer ${accessToken}`;
  }

  // Load image
  const imageUrl = `/api/buildings/${buildingId}/texture`;
  
  // Use fetch to get the image with authentication
  fetch(imageUrl, { headers })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      return response.blob();
    })
    .then(blob => {
      const objectURL = URL.createObjectURL(blob);
      imageEl.src = objectURL;
      imageEl.onload = () => {
        loadingEl.style.display = 'none';
        imageEl.style.display = 'block';
      };
      imageEl.onerror = () => {
        loadingEl.style.display = 'none';
        errorEl.style.display = 'block';
        URL.revokeObjectURL(objectURL);
      };
    })
    .catch(err => {
      console.error('Failed to load texture image:', err);
      loadingEl.style.display = 'none';
      errorEl.style.display = 'block';
    });
}

function setupFilters() {
  const form = document.getElementById('filtersForm');
  const perSelect = document.getElementById('perPageSelect');
  const applyBtn = document.getElementById('applyFilters');

  // Apply button should trigger a reload
  if (applyBtn && form) {
    applyBtn.addEventListener('click', (e) => {
      e.preventDefault();
      load(1);
    });
  }

  // Per-page select change should immediately reload
  if (perSelect) {
    perSelect.addEventListener('change', () => {
      load(1);
    });
  }
}

async function ensureAuthenticated() {
  try {
    // Quick check - apiFetch will attempt a refresh if needed
    await apiFetch('/me', { method: 'GET' });
    return true;
  } catch (e) {
    // Not authenticated -> redirect to login
    try { 
      localStorage.removeItem('pf_refresh_encrypted'); 
      sessionStorage.removeItem('pf_access'); 
    } catch(_) {}
    window.location.href = '/login.html';
    throw e;
  }
}

// Initialize the page
await ensureAuthenticated();
await renderNavbar();
setupCreateModal();
setupFilters();
load();

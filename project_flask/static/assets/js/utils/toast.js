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

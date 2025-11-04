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

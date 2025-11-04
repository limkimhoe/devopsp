import { login } from '../api/authApi.js';
import { apiFetch } from '../auth/fetchClient.js';
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
    // after login, call /me via apiFetch so Authorization header and refresh handling work
    const me = await apiFetch('/me', { method: 'GET' });
    if ((me.roles||[]).includes('admin')) {
      location.href = '/admin/users.html';
    } else {
      location.href = '/me.html';
    }
  }catch(err){
    alertEl.className='alert alert-danger';
    alertEl.textContent = err?.message || 'Login failed';
    alertEl.classList.remove('d-none');
  }
});

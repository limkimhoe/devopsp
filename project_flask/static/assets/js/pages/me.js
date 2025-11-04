import { getMe, patchMe } from '../api/meApi.js';
import { renderNavbar } from '../components/navbar.js';
const form = document.getElementById('meForm');
const account = document.getElementById('accountInfo');

async function init(){
  await renderNavbar();
  try{
    const me = await getMe();
    account.innerHTML = `<div><strong>${me.email}</strong><br>${(me.roles||[]).join(', ')}</div>`;
    // set form values
    Object.entries(me.profile||{}).forEach(([k,v])=>{
      const el = form.elements[k];
      if (el) el.value = v ?? '';
    });
  }catch(e){
    window.location.href = '/login.html';
  }
}
form.addEventListener('submit', async (e)=>{
  e.preventDefault();
  const data = {};
  new FormData(form).forEach((v,k)=> data[k]=v);
  try{
    await patchMe(data);
    alert('Saved');
  }catch(e){
    alert('Save failed');
  }
});
init();

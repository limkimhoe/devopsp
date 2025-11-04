export function serializeForm(form) {
  const data = {};
  new FormData(form).forEach((v,k) => {
    data[k] = v;
  });
  return data;
}
export function setFormValues(form, data) {
  Object.entries(data).forEach(([k,v])=>{
    const input = form.elements[k];
    if (!input) return;
    input.value = v ?? '';
  });
}
export function validateEmail(v){ return /\S+@\S+\.\S+/.test(v); }
export function validateURL(v){ try{ new URL(v); return true }catch(e){ return false } }

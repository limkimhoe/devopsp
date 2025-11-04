export const $ = (s, root=document) => root.querySelector(s);
export const $$ = (s, root=document) => Array.from(root.querySelectorAll(s));
export const el = (tag, props={}, ...children) => {
  const node = document.createElement(tag);
  Object.entries(props).forEach(([k,v]) => node.setAttribute(k,v));
  children.forEach(c => node.append(typeof c === 'string' ? document.createTextNode(c) : c));
  return node;
};
export const show = (el) => el.classList.remove('d-none');
export const hide = (el) => el.classList.add('d-none');

// Client-side filter
const filter = document.getElementById('filter');
const rows = document.getElementById('rows');

filter?.addEventListener('input', () => {
  const q = filter.value.toLowerCase();
  for (const tr of rows.querySelectorAll('tr')) {
    const title = tr.querySelector('.title')?.textContent.toLowerCase() || '';
    const price = tr.querySelector('.price')?.textContent.toLowerCase() || '';

    tr.style.display = (title.includes(q) || price.includes(q)) ? '' : 'none';
  }
});

// Edit modal populate
const editModal = document.getElementById('editModal');
editModal?.addEventListener('show.bs.modal', (ev) => {
  const btn = ev.relatedTarget;
  document.getElementById('edit-id').value    = btn.getAttribute('data-id');
  document.getElementById('edit-title').value = btn.getAttribute('data-title');
  document.getElementById('edit-price').value = btn.getAttribute('data-price');
});

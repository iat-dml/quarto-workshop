document.querySelectorAll('.card[data-href]').forEach(el => {
  el.style.cursor = 'pointer';
  el.addEventListener('click', () => location.href = el.dataset.href);
});

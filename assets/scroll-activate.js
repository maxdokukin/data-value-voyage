document.addEventListener('DOMContentLoaded', () => {
  const methodsToggle = document.getElementById('methodsToggle');
  const dropdown      = methodsToggle.querySelector('.dropdown-content');
  methodsToggle.addEventListener('click', e => {
    e.preventDefault();
    dropdown.classList.toggle('show');
  });
  document.addEventListener('click', e => {
    if (!methodsToggle.contains(e.target)) {
      dropdown.classList.remove('show');
    }
  });
  // …plus your open‑on‑slide‑1 and scroll logic…
});

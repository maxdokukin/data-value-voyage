function toggleTopNav() {
    const topNav = document.getElementById('topNav');
    const topBar = document.getElementById('topBar');
    const menuToggle = document.getElementById('menuToggle');
    if (topNav) topNav.classList.toggle('open');
    if (topBar) topBar.classList.toggle('with-background');
    if (menuToggle) menuToggle.classList.toggle('active');
}

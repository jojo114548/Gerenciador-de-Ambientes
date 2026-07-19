const navbar = document.querySelector('.navbar-lateral');
const toggle = document.getElementById('menuToggle');
const overlay = document.getElementById('menuOverlay');

function abrirMenu() {
  navbar.classList.add('active');
  overlay.classList.add('active');
}

function fecharMenu() {
  navbar.classList.remove('active');
  overlay.classList.remove('active');
}

toggle.addEventListener('click', abrirMenu);
overlay.addEventListener('click', fecharMenu);
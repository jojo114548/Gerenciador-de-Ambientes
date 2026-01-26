function abrirModalDetalhesAmbiente(btn) {
   document.getElementById('modal-detalhes-ambiente').style.display = 'block';
  const card = btn.closest('.card');

const imgCard = card.querySelector('.ambiente-imagem');
  const imgModal = document.getElementById('md-imagem');

  if (imgCard && imgCard.src) {
    imgModal.src = imgCard.src;
    imgModal.style.display = 'block';
  } else {
    imgModal.style.display = 'none';
  }


  document.getElementById('md-nome').textContent =
    card.querySelector('.ambiente-nome').textContent;

  document.getElementById('md-descricao').textContent =
    card.querySelector('.ambiente-descricao').textContent;

  document.getElementById('md-status').textContent =
    card.querySelector('.ambiente-status').textContent;

  document.getElementById('md-capacidade').textContent =
    card.querySelector('.ambiente-capacidade').textContent;

  document.getElementById('md-localizacao').textContent =
    card.querySelector('.ambiente-localizacao').textContent;

  const recursosContainer = card.querySelector('.recursos ul');
  const lista = document.getElementById('md-recursos');
  lista.innerHTML = '';

   if (recursosContainer) {
    recursosContainer.querySelectorAll('li').forEach(li => {
      lista.innerHTML += `<li>${li.textContent}</li>`;
    });
  } else {
    lista.innerHTML = '<li>Não informado</li>';
  }


 
}

function fecharModalDetalhesAmbiente() {
  document.getElementById('modal-detalhes-ambiente').style.display = 'none';
}
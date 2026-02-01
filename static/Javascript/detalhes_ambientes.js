function abrirModalDetalhesAmbiente(btn) {
  const modal = document.getElementById('modal-detalhes-ambiente');
  modal.style.display = 'block';

  const card = btn.closest('.card');

  // Imagem
  const imgModal = document.getElementById('md-imagem');
  const img = card.querySelector('.ambiente-imagem');
  if (img && img.src) {
    imgModal.src = img.src;
    imgModal.style.display = 'block';
  } else {
    imgModal.style.display = 'none';
  }

  // Dados básicos
  document.getElementById('md-nome').textContent =
    card.dataset.ambienteNome || 'Não informado';

  document.getElementById('md-descricao').textContent =
    card.dataset.ambienteDescricao || 'Sem descrição disponível';

  document.getElementById('md-status').textContent =
    card.dataset.ambienteStatus || '—';

  document.getElementById('md-capacidade').textContent =
    card.dataset.ambienteCapacidade
      ? `${card.dataset.ambienteCapacidade} pessoas`
      : '—';

  document.getElementById('md-localizacao').textContent =
    card.dataset.ambienteLocalizacao || 'Não informado';

  // Recursos
  const lista = document.getElementById('md-recursos');
  lista.innerHTML = '';

  if (card.dataset.ambienteRecursos) {
    card.dataset.ambienteRecursos.split('|').forEach(r => {
      const li = document.createElement('li');
      li.textContent = r;
      lista.appendChild(li);
    });
  } else {
    lista.innerHTML = '<li>Não informado</li>';
  }
}


function fecharModalDetalhesAmbiente() {
  document.getElementById('modal-detalhes-ambiente').style.display = 'none';
}
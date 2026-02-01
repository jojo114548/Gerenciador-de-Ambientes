// ===============================
// Modal detalhes equipamento
// ===============================
function abrirModalDetalhesEquipamento(btn) {
  document.getElementById('modal-detalhes-equipamento').style.display = 'block';

  const card = btn.closest('.card');

  // ===============================
  // Imagem
  // ===============================
  const imgCard = card.querySelector('.equipamentos-imagem');
  const imgModal = document.getElementById('md-equip-imagem');

  if (imgCard && imgCard.src) {
    imgModal.src = imgCard.src;
    imgModal.style.display = 'block';
  } else {
    imgModal.style.display = 'none';
  }

  // ===============================
  // Dados básicos
  // ===============================
  document.getElementById('md-equip-nome').textContent =
    card.querySelector('.equipamento-nome')?.textContent || '';

  document.getElementById('md-equip-categoria').textContent =
    card.querySelector('.equipamento-categoria')?.textContent || '-';

  document.getElementById('md-equip-status').textContent =
    card.querySelector('.equipamento-status')?.textContent || '-';

  document.getElementById('md-equip-marca').textContent =
    card.querySelector('.equipamento-marca')?.textContent || '-';

  document.getElementById('md-equip-modelo').textContent =
    card.querySelector('.equipamento-modelo')?.textContent || '-';

  document.getElementById('md-equip-condicao').textContent =
    card.querySelector('.equipamento-condicao')?.textContent || '-';

  document.getElementById('md-equip-descricao').textContent =
    card.querySelector('.equipamento-descricao')?.textContent || '';

  // ===============================
  // 🔹 NOVO — Quantidade disponível
  // ===============================
  document.getElementById('md-equip-quantidade').textContent =
    card.querySelector('.equipamento-quantidade')?.textContent || '0';

  // ===============================
  // Recursos / Especificações
  // ===============================
  const recursosCard = card.querySelector('.recursos-equip ul');
  const lista = document.getElementById('md-equip-recursos');
  lista.innerHTML = '';

  if (recursosCard) {
    recursosCard.querySelectorAll('li').forEach(li => {
      lista.innerHTML += `<li>${li.textContent}</li>`;
    });
  } else {
    lista.innerHTML = '<li>Não informado</li>';
  }
}

// ===============================
// Fechar modal
// ===============================
function fecharModalDetalhesEquipamento() {
  document.getElementById('modal-detalhes-equipamento').style.display = 'none';
}

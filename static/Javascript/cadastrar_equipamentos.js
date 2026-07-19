//  Abrir modal
function abrirModalEquipamento() {
  document.getElementById('modalEquipamento').style.display = 'block';
}

//  Fechar modal
function fecharModalEquipamento() {
  document.getElementById('modalEquipamento').style.display = 'none';
}

//  Adicionar campo de especificação
function addEspecificacao() {
  const container = document.getElementById('especificacoes-container');

  const input = document.createElement('input');
  input.type = 'text';
  input.name = 'especificacao[]';
  input.placeholder = 'Ex: HDMI';

  container.appendChild(input);
}

// Envio do formulário
document.getElementById('form-cadastro-equipamento') .addEventListener('submit', function (e) {

    e.preventDefault();

    const form = this;
    const quantidadeInput = document.getElementById('quantidade_disponivel');

    //  Validação obrigatória (MySQL NOT NULL)
    const quantidade = parseInt(quantidadeInput.value, 10);

    if (isNaN(quantidade) || quantidade < 0) {
      mostrarToast("Informe uma quantidade disponível válida.", "erro");
      quantidadeInput.focus();
      return;
    }

    const formData = new FormData(form);

    // Garantia explícita (opcional, mas seguro)
    formData.set('quantidade_disponivel', quantidade);

    fetch('/equipamento', {
      method: 'POST',
      body: formData
    })
      .then(res => {
        if (!res.ok) throw new Error();
        return res.text();
      })
      .then(() => {
        mostrarToast("Equipamento cadastrado com sucesso", "sucesso");
        fecharModalEquipamento();
        location.reload();
      })
      .catch(() => {
        mostrarToast("Erro ao cadastrar equipamento", "erro");
      });
  });

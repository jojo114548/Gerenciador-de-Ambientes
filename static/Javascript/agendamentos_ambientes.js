function abrirModalAgendamento(id, nome) {
    document.getElementById("modal-agendamento").style.display = "flex";

    document.getElementById("ambiente_id").value = id;
    document.getElementById("titulo-modal").innerText =
        `Novo Agendamento - ${nome}`;
}

document.getElementById('form-agendamento').addEventListener('submit', function(e) {
  e.preventDefault();

  const dados = {
    ambiente_id: document.getElementById('ambiente_id').value,
    data: document.getElementById('ambiente-data').value,
    hora_inicio: document.getElementById('ambiente-hora_inicio').value,
    hora_fim: document.getElementById('ambiente-hora_fim').value,
    finalidade: document.getElementById('ambiente-finalidade').value,
    status: 'pendente'
  };

  fetch('/agendamentos', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dados)
  })
  .then(async response => {
    const res = await response.json();

    // CONFLITO DE HORÁRIO
    if (response.status === 409) {
      console.error("Conflito de horário:", res);
      mostrarToast(res.message || "Este horário já está reservado", "erro");
      return; // ✅ Impede a execução do código de sucesso
    }

    // OUTROS ERROS
    if (!response.ok) {
      console.error("Erro ao agendar:", res);
      mostrarToast(res.message || "Erro ao agendar", "erro");
      return; // ✅ Impede a execução do código de sucesso
    }

    // SUCESSO (só chega aqui se response.ok for true)
    mostrarToast("Agendamento realizado com sucesso", "sucesso");
    fecharModalAgendamento();
    location.reload();
  })
  .catch(err => {
    console.error("Erro de conexão:", err);
    mostrarToast("Erro de conexão", "erro");
  });
});

function fecharModalAgendamento() {
  document.getElementById('modal-agendamento').style.display = 'none';
}
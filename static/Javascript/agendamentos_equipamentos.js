// modal agendamento equipamento
function abrirModalAgendamentoEquipamento(id, nome) {
   document.getElementById("modal-equipamento").style.display = "flex";
   document.getElementById("equipamento_id").value = id;
   document.getElementById("titulo-modal-equip").innerText = `Novo Agendamento - ${nome}`;
}

function fecharModalAgendamentoEquipamento() {
  document.getElementById('modal-equipamento').style.display = 'none';
}

document.addEventListener("DOMContentLoaded", function () {

  const form = document.getElementById("form-agendamento-equipamento");

  if (!form) {

   mostrarToast("Formulário NÃO encontrado", "erro");
    return;
  }

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    // ✅ CORRIGIDO: Enviando 'data' em vez de 'data_equip'
    const dados = {
      equipamento_id: document.getElementById('equipamento_id').value,
      data: document.getElementById('equipamento-data_equip').value,  // ← MUDOU AQUI
      hora_inicio: document.getElementById('equipamento-hora_inicio').value,
      hora_fim: document.getElementById('equipamento-hora_fim').value,
      finalidade: document.getElementById('equipamento-finalidade').value,
      status: 'pendente'
    };

    try {
      const response = await fetch('/agendamentos_equipamentos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados)
      });

      const res = await response.json();

      // CONFLITO DE HORÁRIO
      if (response.status === 409) {
        mostrarToast("Conflito de horário", "erro");
        return;
      }

      // OUTROS ERROS
      if (!response.ok) {
        console.error("Erro ao agendar:", res);
        mostrarToast("Erro ao agendar", "erro");
      }

      // SUCESSO
      mostrarToast("Agendamento realizado com sucesso", "sucesso");
      fecharModalAgendamentoEquipamento(); 
      location.reload();

    } catch (err) {
      mostrarToast("Erro de conexão", "erro");
    }
  });
});
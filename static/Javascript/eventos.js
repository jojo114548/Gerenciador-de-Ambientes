
//deletar eventos
async function deletarAgendamento(id) {
  if (!confirm("Deseja realmente excluir este agendamento?")) return;

  try {
    const response = await fetch(`/eventos/${id}`, {
      method: "DELETE"
    });

    const result = await response.json();

    if (response.ok) {
      alert("Agendamento excluído");
      location.reload();
    } else {
      alert(result.erro || "Erro ao excluir");
    }
  } catch (error) {
    console.error(error);
    alert("Erro de conexão");
  }
}


//inscrever em eventos
async function inscreverEvento(eventoId) {
  try {
    const response = await fetch(`/eventos/${eventoId}/inscrever`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      }
    });

    const result = await response.json();

    if (response.ok) {
      alert("Inscrição realizada com sucesso");
      location.reload();
    } else {
      alert(result.erro || "Erro ao se inscrever");
    }

  } catch (err) {
    console.error(err);
    alert("Erro de conexão");
  }
}



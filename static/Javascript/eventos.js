//deletar eventos
async function deletarAgendamento(id) {
  if (!confirm("Deseja realmente excluir este agendamento?")) return;

  try {
    const response = await fetch(`/eventos/${id}`, {
      method: "DELETE"
    });

    const result = await response.json();

    if (response.ok) {
      mostrarToast("Agendamento excluído", "sucesso");
      setTimeout(() => location.reload(), 1200); // dá tempo de ver o toast
    } else {
      mostrarToast(result.erro || "Erro ao excluir", "erro");
    }
  } catch (error) {
    console.error(error);
    mostrarToast("Erro de conexão", "erro");
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
      mostrarToast("Inscrição realizada com sucesso", "sucesso");
      setTimeout(() => location.reload(), 1200);
    } else {
      mostrarToast(result.erro || "Erro ao se inscrever", "erro");
    }

  } catch (err) {
    console.error(err);
    mostrarToast("Erro de conexão", "erro");
  }
}

function scrollCarousel(id, direction) {
    const track = document.getElementById(id);
    if (!track) return;

    const card = track.querySelector('.event-card');
    const cardWidth = card ? card.offsetWidth + 20 : 320; // largura + gap

    track.scrollBy({
        left: direction * cardWidth,
        behavior: 'smooth'
    });
}
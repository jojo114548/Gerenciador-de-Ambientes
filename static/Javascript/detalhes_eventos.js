function abrirModalDetalhes(btn) {
  console.log("=== ABRINDO MODAL DE DETALHES ===");
  
  // Verificar modal
  const modal = document.getElementById("modaldetalhes");
  if (!modal) {
    alert("Erro: Modal não encontrado!");
    console.error("❌ Modal 'modaldetalhes' não existe no HTML");
    return;
  }

  modal.classList.add("active");

  // Buscar o card do evento
  const card = btn.closest(".event-card") || btn.closest("tr.event-card");
  
  if (!card) {
    alert("Erro: Evento não encontrado!");
    console.error("❌ Card do evento não encontrado");
    return;
  }

  console.log("✅ Card encontrado");

  // Função segura para definir texto
  const setTextSafe = (id, value) => {
    const el = document.getElementById(id);
    if (el) {
      el.textContent = value || "Não informado";
      return true;
    } else {
      console.warn(`⚠️ Elemento '${id}' não encontrado no modal`);
      return false;
    }
  };

  // Função segura para obter texto
  const getTextSafe = (selector) => {
    try {
      const el = card.querySelector(selector);
      return el ? el.textContent.trim() : "";
    } catch (e) {
      console.warn(`⚠️ Erro ao buscar '${selector}':`, e);
      return "";
    }
  };

  // Capturar dados
  const titulo = getTextSafe(".event-titulo");
  const data = getTextSafe(".event-data");
  const hora = getTextSafe(".event-hora");
  const local = getTextSafe(".event-local");
  const descricao = getTextSafe(".event-desc");
  const instrutor = getTextSafe(".event-instrutor");
  const ambiente = getTextSafe(".event-ambiente");

  console.log("Dados capturados:", { titulo, data, hora, local, instrutor });

  // Preencher campos básicos
  setTextSafe("md-titulo", titulo || "Sem título");
  setTextSafe("md-tipo", "Evento");
  setTextSafe("md-data", data || "Data não disponível");
  setTextSafe("md-hora", hora || "Horário não disponível");
  setTextSafe("md-local", local || ambiente || "Local não disponível");
  setTextSafe("md-descricao", descricao || "Sem descrição disponível");
  setTextSafe("md-instrutor", instrutor || "Não informado");
  setTextSafe("md-ambiente", ambiente || local || "Não informado");

  // Configurar imagem
  try {
    const imgCard = card.querySelector(".eventos-imagem");
    const imgModal = document.getElementById("md-image");
    
    if (imgModal && imgCard && imgCard.src && imgCard.src !== window.location.href && !imgCard.src.includes("/None")) {
      imgModal.src = imgCard.src;
      imgModal.style.display = "block";
    } else if (imgModal) {
      imgModal.style.display = "none";
    }
  } catch (e) {
    console.warn("⚠️ Erro ao configurar imagem:", e);
  }

  // Calcular capacidade
  try {
    const capacidadeEl = card.querySelector(".event-capacidade");
    const participantes = parseInt(capacidadeEl?.dataset?.participantes || 0);
    const maxCapacidade = parseInt(capacidadeEl?.dataset?.capacidade || 0);
    const vagasRestantes = maxCapacidade - participantes;

    setTextSafe("md-capacidade", `${participantes}/${maxCapacidade} participantes`);
    setTextSafe("md-vagas", vagasRestantes > 0 ? vagasRestantes : "Esgotado");

    console.log("Capacidade:", { participantes, maxCapacidade, vagasRestantes });
  } catch (e) {
    console.warn("⚠️ Erro ao calcular capacidade:", e);
    setTextSafe("md-capacidade", "0/0");
    setTextSafe("md-vagas", "0");
  }

  // Configurar botão de ação
  try {
    const actions = document.getElementById("md-actions");
    if (!actions) {
      console.error("❌ Elemento 'md-actions' não encontrado");
      return;
    }

    const eventId = card.dataset?.eventId || "";
    const inscrito = card.dataset?.inscrito === "true";
    const capacidadeEl = card.querySelector(".event-capacidade");
    const participantes = parseInt(capacidadeEl?.dataset?.participantes || 0);
    const maxCapacidade = parseInt(capacidadeEl?.dataset?.capacidade || 0);

    actions.innerHTML = "";

    if (inscrito) {
      actions.innerHTML = `
        <button class="btn-reserve btn-inscrito" disabled style="background: #dbeafe; color: #1e40af; padding: 10px 20px; border: none; border-radius: 8px; cursor: not-allowed;">
          ✓ Você está inscrito
        </button>
      `;
    } else if (participantes >= maxCapacidade) {
      actions.innerHTML = `
        <button class="btn-reserve btn-lotado" disabled style="background: #fee2e2; color: #991b1b; padding: 10px 20px; border: none; border-radius: 8px; cursor: not-allowed;">
          Evento Lotado
        </button>
      `;
    } else {
      actions.innerHTML = `
        <button class="btn-reserve" onclick="inscreverEvento('${eventId}')" style="background: #3b82f6; color: white; padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;">
          Inscrever-se no Evento
        </button>
      `;
    }

    console.log("✅ Botão configurado");
  } catch (e) {
    console.error("❌ Erro ao configurar botão:", e);
  }

  console.log("✅ Modal preenchido com sucesso!");
}

function fecharModalDetalhes() {
  const modal = document.getElementById("modaldetalhes");
  if (modal) {
    modal.classList.remove("active");
  }
}

// Fechar modal ao clicar fora
document.addEventListener('DOMContentLoaded', function() {
  console.log("=== Script detalhes_eventos.js carregado ===");
  
  const modal = document.getElementById("modaldetalhes");
  
  if (modal) {
    console.log("✅ Modal encontrado no DOM");
    modal.addEventListener('click', function(e) {
      if (e.target === modal) {
        fecharModalDetalhes();
      }
    });
  } else {
    console.warn("⚠️ Modal 'modaldetalhes' não encontrado no carregamento");
  }

  const cards = document.querySelectorAll('.event-card');
  console.log(`📊 Total de eventos: ${cards.length}`);
});
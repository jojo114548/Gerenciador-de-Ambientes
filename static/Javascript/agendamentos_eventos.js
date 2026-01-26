// ================================
// CONTROLE DO MODAL
// ================================
function abrirModal() {
  const modal = document.getElementById("modalAgendamento");
  if (modal) modal.style.display = "flex";
}

function fecharModal() {
  const modal = document.getElementById("modalAgendamento");
  const form = document.getElementById("formEvento");

  if (modal) modal.style.display = "none";
  if (form) form.reset();

  const container = document.getElementById("equipamentos-container");
  if (!container) return;

  const items = container.querySelectorAll(".equipamento-item");
  items.forEach((item, index) => {
    if (index > 0) item.remove();
  });
}

// ================================
// GERENCIAMENTO DE EQUIPAMENTOS
// ================================
function adicionarEquipamento() {
  const container = document.getElementById("equipamentos-container");
  if (!container) return;

  const primeiroItem = container.querySelector(".equipamento-item");
  if (!primeiroItem) return;

  const novoItem = primeiroItem.cloneNode(true);

  novoItem.querySelector("select").value = "";
  novoItem.querySelector("input").value = "1";

  const btnRemove = novoItem.querySelector(".btn-remove-equipamento");
  if (btnRemove) btnRemove.style.display = "block";

  container.appendChild(novoItem);
  atualizarBotoesRemover();
}

function removerEquipamento(button) {
  button.closest(".equipamento-item")?.remove();
  atualizarBotoesRemover();
}

function atualizarBotoesRemover() {
  const container = document.getElementById("equipamentos-container");
  if (!container) return;

  const items = container.querySelectorAll(".equipamento-item");
  items.forEach(item => {
    const btn = item.querySelector(".btn-remove-equipamento");
    if (btn) btn.style.display = items.length > 1 ? "block" : "none";
  });
}

// ================================
// AMBIENTE / CAPACIDADE
// ================================
function atualizarCapacidadeAmbiente() {
  const select = document.getElementById("ambiente_id");
  const infoDiv = document.getElementById("ambiente-info");
  const capacidadeInput = document.getElementById("capacidade");
  const hintDiv = document.getElementById("capacidade-hint");

  if (!select || !capacidadeInput) return;

  const option = select.options[select.selectedIndex];
  const capacidade = option?.getAttribute("data-capacidade");

  if (capacidade) {
    infoDiv.textContent = `Capacidade máxima do ambiente: ${capacidade} pessoas`;
    capacidadeInput.max = capacidade;
    if (hintDiv) {
      hintDiv.textContent = `Máximo permitido para este ambiente: ${capacidade}`;
    }
  } else {
    infoDiv.textContent = "";
    capacidadeInput.removeAttribute("max");
    if (hintDiv) hintDiv.textContent = "";
  }
}

// ================================
// VERIFICAR DISPONIBILIDADE
// ================================
async function verificarDisponibilidade() {
  const ambiente_id = document.getElementById("ambiente_id")?.value;
  const data_evento = document.getElementById("data_evento")?.value;
  const hora_evento = document.getElementById("hora_evento")?.value;

  if (!ambiente_id || !data_evento || !hora_evento) {
    alert("Preencha o ambiente, data e horário para verificar disponibilidade");
    return;
  }

  const equipamentos = [];
  const equipSelects = document.querySelectorAll('select[name="equipamentos[]"]');
  const quantInputs = document.querySelectorAll('input[name="quantidades[]"]');

  equipSelects.forEach((select, index) => {
    if (select.value) {
      equipamentos.push({
        equipamento_id: parseInt(select.value),
        quantidade: parseInt(quantInputs[index]?.value || 1)
      });
    }
  });

  try {
    const response = await fetch("/api/verificar-disponibilidade", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ambiente_id,
        data_evento,
        hora_evento,
        equipamentos
      })
    });

    const result = await response.json();

    if (result.ambiente_disponivel && result.equipamentos_disponiveis) {
      alert("✅ Todos os recursos estão disponíveis!");
    } else {
      alert(`⚠️ ${result.mensagens?.join("\n") || "Recursos indisponíveis"}`);
    }

  } catch (error) {
    console.error(error);
    alert("Erro ao verificar disponibilidade");
  }
}

// ================================
// SUBMISSÃO DO FORMULÁRIO
// ================================
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("formEvento");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);

    const equipamentos = formData.getAll("equipamentos[]");
    const quantidades = formData.getAll("quantidades[]");

    formData.delete("equipamentos[]");
    formData.delete("quantidades[]");

    equipamentos.forEach((equip, index) => {
      if (equip) {
        formData.append("equipamentos[]", equip);
        formData.append("quantidades[]", quantidades[index] || 1);
      }
    });

    try {
      const response = await fetch("/eventos", {
        method: "POST",
        body: formData
      });

      const result = await response.json();

      if (response.ok) {
        alert("✅ Evento criado com sucesso!");
        location.reload();
      } else {
        alert(result.erro || "Erro ao criar evento");
      }

    } catch (error) {
      console.error(error);
      alert("Erro de conexão");
    }
  });
});

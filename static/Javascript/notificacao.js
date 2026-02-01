/* ======================================================
   FECHAR MODAL
====================================================== */
function fecharmodal() {
  document
    .getElementById("modal-notificacoes")
    .classList.remove("active");
}

/* ======================================================
   ABRIR MODAL + BUSCAR NOTIFICAÇÕES
====================================================== */
async function modal_notificacao() {
  const usuarioId = "admin";

  const res = await fetch(`/notificacoes/${usuarioId}`);
  const dados = await res.json();

  const modal = document.getElementById("modal-notificacoes");
  const lista = document.getElementById("lista-notificacoes");
  const badge = document.getElementById("badge-notificacao");

  modal.classList.add("active");

  /* ===== BADGE ===== */
  const naoLidas = dados.filter(n => !n.lida).length;

  if (naoLidas > 0) {
    badge.textContent = naoLidas;
    badge.style.display = "flex";
  } else {
    badge.style.display = "none";
  }

  /* ===== LISTA ===== */
  if (!dados.length) {
    lista.innerHTML = `
      <div class="notificacao-vazia">
        Nenhuma notificação
      </div>`;
    return;
  }

  lista.innerHTML = dados.map(n => `
    <div class="
      notificacao-item
      ${!n.lida ? "nao-lida" : ""}
      ${n.tipo || "info"}
    " data-id="${n.id}">
      <span class="notificacao-titulo">${n.titulo}</span>
      <span class="notificacao-mensagem">${n.mensagem}</span>
      <span class="notificacao-data">${n.data || ""}</span>
    </div>
  `).join("");
}

/* ======================================================
   MARCAR COMO LIDA (CLICK)
====================================================== */
document.getElementById("lista-notificacoes").addEventListener("click", async e => {
  const item = e.target.closest(".notificacao-item");
  if (!item) return;

  const id = item.dataset.id;

  await fetch(`/notificacoes/${id}/lida`, {
    method: "PUT"
  });

  /* Atualiza visualmente sem fechar */
  item.classList.remove("nao-lida");

  /* Recalcula badge */
  atualizarBadge();
});

/* ======================================================
   ATUALIZAR BADGE (REUSO)
====================================================== */
async function atualizarBadge() {
  const usuarioId = "admin";
  const badge = document.getElementById("badge-notificacao");

  const res = await fetch(`/notificacoes/${usuarioId}`);
  const dados = await res.json();

  const naoLidas = dados.filter(n => !n.lida).length;

  if (naoLidas > 0) {
    badge.textContent = naoLidas;
    badge.style.display = "flex";
  } else {
    badge.style.display = "none";
  }
}

/* ======================================================
   INICIALIZA BADGE AO CARREGAR
====================================================== */
document.addEventListener("DOMContentLoaded", atualizarBadge);

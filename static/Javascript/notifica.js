// cria o container de toasts se ainda não existir
function getToastContainer() {
  let container = document.querySelector(".toast-container");
  if (!container) {
    container = document.createElement("div");
    container.className = "toast-container";
    document.body.appendChild(container);
  }
  return container;
}

// tipo: "sucesso" | "erro" | "info"
function mostrarToast(mensagem, tipo = "info") {
  const container = getToastContainer();

  const toast = document.createElement("div");
  toast.className = `toast toast-${tipo}`;
  toast.textContent = mensagem;

  container.appendChild(toast);

  // remove do DOM depois que a animação de saída termina (3s + 0.3s)
  setTimeout(() => {
    toast.remove();
  }, 3300);
}
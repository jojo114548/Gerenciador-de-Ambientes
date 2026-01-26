function modalConfig(event) {
  if (event) event.preventDefault();
  document.querySelector(".modal-configuracao").style.display = "flex";

  // Abre Perfil por padrão
  document.querySelector(".modal-perfil").style.display = "block";
  document.querySelector(".modal-seguranca").style.display = "none";
  document.querySelector(".modal-privacidade").style.display = "none";
}

function FecharConfig() {
  document.querySelector(".modal-configuracao").style.display = "none";
}

function perfil() {
 document.querySelector(".modal-perfil").style.display = "block";
  document.querySelector(".modal-seguranca").style.display = "none";
  document.querySelector(".modal-privacidade").style.display = "none";

}

function modalSeguranca() {
  document.querySelector(".modal-perfil").style.display = "none";
  document.querySelector(".modal-seguranca").style.display = "block";
  document.querySelector(".modal-privacidade").style.display = "none";
}

function privacidade() {
  document.querySelector(".modal-perfil").style.display = "none";
  document.querySelector(".modal-seguranca").style.display = "none";
  document.querySelector(".modal-privacidade").style.display = "block";
}

function alterarSenha(event) {
  if (event) event.preventDefault();

   const usuarioId = document.getElementById("edit-user-id")?.value || "{{ id_logado }}";

  const senhaNova = document.getElementById("senha-nova").value.trim();
  const confirmar = document.getElementById("confirmar-senha").value.trim();

  if (!senhaNova || !confirmar) {
    alert("Preencha todos os campos");
    return;
  }

  if (senhaNova !== confirmar) {
    alert("As senhas não coincidem");
    return;
  }

  fetch(`/usuarios/${usuarioId}/senha`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json"
    },
    credentials: "include",
    body: JSON.stringify({ senha: senhaNova })
  })
    .then(res => res.json())
    .then(res => {
      if (res.erro) {
        alert(res.erro);
        return;
      }

      alert("Senha alterada com sucesso");

      document.getElementById("senha-nova").value = "";
      document.getElementById("confirmar-senha").value = "";

      // Volta para Perfil
      perfil();
    })
    .catch(() => {
      alert("Erro ao alterar senha");
    });
}

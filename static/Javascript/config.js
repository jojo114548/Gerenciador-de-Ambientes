function modalConfig(event) {
  if (event) event.preventDefault();
  document.querySelector(".modal-configuracao").style.display = "flex";

  // Abre Perfil por padrão
  document.querySelector(".modal-perfil").style.display = "block";
  document.querySelector(".modal-seguranca").style.display = "none";
}

function FecharConfig() {
  document.querySelector(".modal-configuracao").style.display = "none";
}

function perfil() {
  document.querySelector(".modal-perfil").style.display = "block";
  document.querySelector(".modal-seguranca").style.display = "none";
   document.querySelector(".modal-excluir").style.display = "none";
}

function modalSeguranca() {
  document.querySelector(".modal-perfil").style.display = "none";
  document.querySelector(".modal-seguranca").style.display = "block";
    document.querySelector(".modal-excluir").style.display = "none";
}
function ApagarConta(){
     document.querySelector(".modal-excluir").style.display = "block";
    document.querySelector(".modal-perfil").style.display = "none";
  document.querySelector(".modal-seguranca").style.display = "none";
 
}
function alterarSenha(event) {
  if (event) event.preventDefault();

  // ✅ Pega o ID do data-attribute do formulário
  const form = document.getElementById("form-alterar-senha");
  const usuarioId = form.getAttribute("data-user-id");

  const senhaAtual = document.getElementById("senha-atual").value.trim();
  const senhaNova = document.getElementById("senha-nova").value.trim();
  const confirmar = document.getElementById("confirmar-senha").value.trim();

  // Validações
  if (!senhaAtual || !senhaNova || !confirmar) {
    alert("Preencha todos os campos");
    return;
  }

  if (senhaNova !== confirmar) {
    alert("As senhas não coincidem");
    return;
  }

  if (senhaAtual === senhaNova) {
    alert("A nova senha não pode ser igual à senha atual");
    return;
  }

  if (senhaNova.length < 6) {
    alert("A senha deve ter no mínimo 6 caracteres");
    return;
  }

  fetch(`/usuarios/${usuarioId}/senha`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json"
    },
    credentials: "include",
    body: JSON.stringify({ 
      senha_atual: senhaAtual,
      senha_nova: senhaNova 
    })
  })
    .then(res => res.json())
    .then(res => {
      if (res.erro) {
        alert(res.erro);
        return;
      }

      alert(res.mensagem || "Senha alterada com sucesso");

      // Limpa os campos
      document.getElementById("senha-atual").value = "";
      document.getElementById("senha-nova").value = "";
      document.getElementById("confirmar-senha").value = "";

      // Volta para Perfil
      perfil();
    })
    .catch(error => {
      console.error("Erro:", error);
      alert("Erro ao alterar senha");
    });
}

function excluirUsuario(id) {
    if (!confirm("Tem certeza que deseja excluir sua conta? Essa ação é irreversível.")) {
        return;
    }



    fetch(`/usuarios/${id}`, {
        method: 'DELETE',
        credentials: 'include' // 🔐 envia JWT (OBRIGATÓRIO)
    })
    .then(response => response.json().then(data => {
        if (!response.ok) {
            throw new Error(data.erro || "Erro desconhecido");
        }
        return data;
    }))
    .then(data => {
        alert(data.mensagem);

        //  desloga após excluir a própria conta
        window.location.href = "/logout";
    })
    .catch(error => {
        console.error("Erro ao excluir conta:", error);
        alert("Erro ao excluir conta: " + error.message);
    });
}

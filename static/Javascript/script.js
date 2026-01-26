// ====================== EXCLUIR USUÁRIO ======================
function excluirUsuario(cpf, id) {
    if (!confirm(`Tem certeza que deseja excluir o usuário com CPF: ${cpf}?`)) {
        return;
    }

    fetch(`/usuarios/${id}`, {
        method: 'DELETE'
    })
    .then(response => response.json().then(data => {
        if (!response.ok) {
            throw new Error(data.erro || "Erro desconhecido");
        }
        return data;
    }))
    .then(data => {
        alert(data.mensagem);
        if (data.mensagem.includes("deslogado")) {
            window.location.href = "/login";
        } else {
            location.reload();
        }
    })
    .catch(error => {
        console.error("Erro na requisição", error);
        alert("Erro ao excluir usuário: " + error.message);
    });
}


// ====================== PREENCHER FORMULÁRIO ======================
function preencherFormulario(button) {
    const container = document.querySelector(".container");
    const usuario = JSON.parse(button.getAttribute('data-usuario'));

    container.style.display = "grid"; // mostra o formulário
    document.getElementById('id').value = usuario.id;
    document.getElementById('nome').value = usuario.nome;
    document.getElementById('email').value = usuario.email;
    document.getElementById('idade').value = usuario.idade;
    document.getElementById('cpf').value = usuario.cpf;
    document.getElementById('perfil').value = usuario.perfil;
    if (document.getElementById('senha')) {
        document.getElementById('senha').value = ""; // limpa campo de senha
    }
}


// ====================== ATUALIZAR USUÁRIO ======================
document.getElementById('form-atualizar-usuario').addEventListener('submit', atualizarUsuario);

function atualizarUsuario(event) {
    event.preventDefault();

    if (!confirm("Tem certeza que deseja alterar os dados do usuário?")) {
        return;
    }

    const id = document.getElementById('id').value;

    const dadosUsuario = {
        nome: document.getElementById('nome').value,
        cpf: document.getElementById('cpf').value,
        email: document.getElementById('email').value,
        idade: document.getElementById('idade').value,
        perfil: document.getElementById('perfil').value,
    };
    if (document.getElementById('senha')) {
        dadosUsuario.senha = document.getElementById('senha').value;
    }

   fetch(`/usuarios/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(dadosUsuario)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { 
                throw new Error(err.erro || "Erro desconhecido"); 
            });
        }
        return response.json();
    })
    .then(data => {
        alert(data.mensagem);
        location.reload();
    })
    .catch(error => {
        console.error("Erro ao atualizar:", error);
        alert("Erro ao atualizar usuário: " + error.message);
    });
}

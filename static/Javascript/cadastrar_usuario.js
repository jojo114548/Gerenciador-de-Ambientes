function Cadastrar(){
    document.getElementById("cadastrar-user-modal").style.display = "flex";
}

function FecharCadastrar() {
    document.getElementById("cadastrar-user-modal").style.display = "none";
}

const form = document.getElementById("cadastrar-user-Adm");

form.addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(form);

    fetch("/novo-usuario", {
        method: "POST",
        body: formData
    })
    .then(res => {
        if (!res.ok) {
            // ✅ Tente pegar a mensagem de erro do servidor
            return res.json().then(err => {
                throw new Error(err.erro || "Erro ao cadastrar usuário");
            });
        }
        return res.json(); // ✅ Processe como JSON
    })
    .then(() => {
        alert("Usuário cadastrado com sucesso");
        FecharCadastrar();
        form.reset(); // ✅ Limpa o formulário
        window.location.reload();
    })
    .catch(err => {
        console.error("Erro:", err);
        alert(err.message);
    });
});
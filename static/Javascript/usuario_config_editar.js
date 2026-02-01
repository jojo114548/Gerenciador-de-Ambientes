function abrirModalUsuario() {
  document.getElementById("modalUsuarioConfig").style.display = "flex";
}

function fecharModalUsuario() {
  document.getElementById("modalUsuarioConfig").style.display = "none";
}


function abrirEditarUsuario(
   id,
  image,
  name,
  email,
  cpf,
  rg,
  dataNascimento,
  telefone,
  endereco,
  departamento,
  funcao,
  role,
    status

) {
  fecharModalUsuario();

  document.getElementById("edit-config-modal").style.display = "flex";

  document.getElementById("edit-user-id").value = id;
 

  document.getElementById("edit-user-name").value = name ;
  document.getElementById("edit-user-email").value = email ;
  document.getElementById("edit-user-cpf").value = cpf ;
  document.getElementById("edit-user-rg").value = rg ;
  document.getElementById("edit-user-data-nascimento").value = dataNascimento ;
  document.getElementById("edit-user-telefone").value = telefone ;
  document.getElementById("edit-user-endereco").value = endereco ;
  document.getElementById("edit-user-departamento").value = departamento ;
  document.getElementById("edit-user-funcao").value = funcao ;
  document.getElementById("edit-user-role").value = role ;
  document.getElementById("edit-user-status").value = status ;

   

  const preview = document.getElementById("preview-imagem");
  if (preview && image) preview.src = image;
}



document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("edit-config-form");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const id = document.getElementById("edit-user-id").value;

    const formData = new FormData();
    formData.append("name", document.getElementById("edit-user-name").value);
    formData.append("email", document.getElementById("edit-user-email").value);
    formData.append("cpf", document.getElementById("edit-user-cpf").value);
    formData.append("rg", document.getElementById("edit-user-rg").value);
    formData.append("data_nascimento", document.getElementById("edit-user-data-nascimento").value);
    formData.append("telefone", document.getElementById("edit-user-telefone").value);
    formData.append("endereco", document.getElementById("edit-user-endereco").value);
    formData.append("departamento", document.getElementById("edit-user-departamento").value);
    formData.append("funcao", document.getElementById("edit-user-funcao").value);
    formData.append("role", document.getElementById("edit-user-role").value);
    formData.append("status", document.getElementById("edit-user-status").value);
    
    

    const imagemInput = document.getElementById("edit-image-atual");
    if (imagemInput && imagemInput.files.length > 0) {
      formData.append("image", imagemInput.files[0]);
    }

    fetch(`/usuarios/${id}`, {
      method: "PUT",
       credentials: "include",
      body: formData
    })
      .then(res => {
        if (!res.ok) throw new Error();
        return res.json();
      })
      .then(data => {
        alert(data.mensagem || "Usuário atualizado com sucesso");
        fecharEditarUsuario();
        location.reload();
      })
      .catch(() => {
        alert("Erro ao atualizar usuário");
      });
  });
});


function fecharEditarUsuario(){
  document.getElementById("edit-config-modal").style.display = "none";
}
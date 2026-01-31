
function abrirModalAmbiente(){
    document.getElementById('add-ambiente-modal').style.display = 'block';
}

 function addrecursos() {
  const container = document.getElementById('especificacoes-container');
  const input = document.createElement('input');
  input.type = 'text';
  input.name = 'recursos[]';
  input.placeholder = 'Ex: Pojetor';
  input.style.marginBottom = '8px';
  input.style.width = '100%';
  container.appendChild(input);
}

document.getElementById('form-editar-ambiente').addEventListener('submit', function (event) {
    event.preventDefault();

    if (!confirm("Deseja salvar as alterações do ambiente?")) {
        return;
    }

    const id = document.getElementById('edit-id').value;
    const formData = new FormData();

    formData.append('name', document.getElementById('edit-nome').value);
    formData.append('descricao', document.getElementById('edit-descricao').value);
    formData.append('capacidade', document.getElementById('edit-capacidade').value);
    formData.append('status', document.getElementById('edit-status').value);
    formData.append('area', document.getElementById('edit-area').value);
    formData.append('localizacao', document.getElementById('edit-localizacao').value);

    const imagem = document.getElementById('edit-imagem').files[0];
    if (imagem) {
        formData.append('image', imagem);
    }


       // Preencher especificações
  const container = document.querySelectorAll('especificacoes-container input[name="recursos[]');
  container.innerHTML = '';

  if (ambiente.recursos && ambiente.recursos.length > 0) {
    ambiente.recursos.forEach(recursos => {
      const input = document.createElement('input');
      input.type = 'text';
      input.name = 'recursos[]';
      input.value = recursos;
      input.placeholder = 'Ex: Pojetor';
      input.style.marginBottom = '8px';
      input.style.width = '100%';
      container.appendChild(input);
    });
  } else {
    addrecursos();
  }
  
    fetch(`/ambientes/${id}`, {
        method: 'POST',
        body: formData
    })
   .then(res => {
        if (!res.ok) throw new Error('Erro na requisição');
        return res.json();
      })
      .then(data => {
        alert(data.mensagem);
        fecharModalAmbiente();
        location.reload();
      })
      .catch(err => {
        console.error(err);
        alert('Erro ao Cadastrar ambiente');
      });
});



function fecharModalAmbiente(){
   document.getElementById('add-ambiente-modal').style.display = 'none';
   
}

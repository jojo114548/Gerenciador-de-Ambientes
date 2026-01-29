
function abrirModalAmbiente(){
    document.getElementById('add-ambiente-modal').style.display = 'block';
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

    document.querySelectorAll('#recursos-container input[name="recursos[]"]')
        .forEach(cb => formData.append('recursos[]', cb.value));

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

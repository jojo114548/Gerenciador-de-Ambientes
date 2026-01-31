function abrirModalEditar(button) {
  const ambiente = JSON.parse(button.getAttribute('data-ambiente'));

  document.getElementById('modal-editar').style.display = 'block';

  document.getElementById('edit-id').value = ambiente.id;
  document.getElementById('edit-nome').value = ambiente.name;
  document.getElementById('edit-descricao').value = ambiente.descricao || '';
  document.getElementById('edit-capacidade').value = ambiente.capacidade || '';
  document.getElementById('edit-status').value = ambiente.status;
  document.getElementById('edit-area').value = ambiente.area || '';
  document.getElementById('edit-localizacao').value = ambiente.localizacao || '';
  
  // Definir o tipo se existir
  if (ambiente.type) {
    document.getElementById('edit-type').value = ambiente.type;
  }

  const preview = document.getElementById('preview-imagem');
  if (ambiente.image) {
    preview.src = ambiente.image;
    preview.style.display = 'block';
    document.getElementById('edit-image-atual').value = ambiente.image;
  } else {
    preview.style.display = 'none';
  }

  // Listener para mudança de imagem
  document.getElementById('edit-imagem').addEventListener('change', function () {
    const file = this.files[0];
    if (file) {
      preview.src = URL.createObjectURL(file);
      preview.style.display = 'block';
    }
  });

    // Preencher especificações
  const container = document.getElementById('recursos-container');
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
    addrecursosEdit();
  }
}

function addrecursosEdit() {
  const container = document.getElementById('recursos-container');
  const input = document.createElement('input');
  input.type = 'text';
  input.name = 'recursos[]';
  input.placeholder = 'Ex: Pojetor';
  input.style.marginBottom = '8px';
  input.style.width = '100%';
  container.appendChild(input);
}

function fecharModalEditar() {
  document.getElementById('modal-editar').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('form-editar-ambiente');

  if (!form) return;

  form.onsubmit = function (e) {
    e.preventDefault();

    const formData = new FormData(form);
    const id = document.getElementById('edit-id').value;

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
        fecharModalEditar();
        location.reload();
      })
      .catch(err => {
        console.error(err);
        alert('Erro ao atualizar ambiente');
      });
  };
});

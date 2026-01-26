// ===============================
// Modal editar equipamento
// ===============================
function abrirModalEditarEquipamento(button) {
  const equipamento = JSON.parse(button.getAttribute('data-equipamento'));
  
  document.getElementById('modalEditarEquipamento').style.display = 'block';

  // Preencher campos
  document.getElementById('edit_id').value = equipamento.id || '';
  document.getElementById('edit_name').value = equipamento.name || '';
  document.getElementById('edit_categoria').value = equipamento.categoria || '';
  document.getElementById('edit_status').value = equipamento.status || 'Disponivel';
  document.getElementById('edit_marca').value = equipamento.marca || '';
  document.getElementById('edit_modelo').value = equipamento.modelo || '';
  document.getElementById('edit_condicao').value = equipamento.condicao || '';
  document.getElementById('edit_descricao').value = equipamento.descricao || '';
  document.getElementById('edit_quantidade_disponivel').value = equipamento.quantidade_disponivel  || '';

  // Preview da imagem
  const preview = document.getElementById('edit-preview-imagem');
  if (equipamento.image) {
    preview.src = equipamento.image;
    preview.style.display = 'block';
  } else {
    preview.style.display = 'none';
  }

  // Preencher especificações
  const container = document.getElementById('edit-especificacoes-container');
  container.innerHTML = '';

  if (equipamento.especificacoes && equipamento.especificacoes.length > 0) {
    equipamento.especificacoes.forEach(especificacao => {
      const input = document.createElement('input');
      input.type = 'text';
      input.name = 'especificacoes[]';
      input.value = especificacao;
      input.placeholder = 'Ex: USB-C';
      input.style.marginBottom = '8px';
      input.style.width = '100%';
      container.appendChild(input);
    });
  } else {
    addEditEspecificacao();
  }
}

// ===============================
// Fechar modal
// ===============================
function fecharModalEditarEquipamento() {
  document.getElementById('modalEditarEquipamento').style.display = 'none';
  

}

// ===============================
// Adicionar especificação
// ===============================
function addEditEspecificacao() {
  const container = document.getElementById('edit-especificacoes-container');
  const input = document.createElement('input');
  input.type = 'text';
  input.name = 'especificacoes[]';
  input.placeholder = 'Ex: USB-C';
  input.style.marginBottom = '8px';
  input.style.width = '100%';
  container.appendChild(input);
}

// ===============================
// Preview de imagem (listener único)
// ===============================
document.addEventListener('DOMContentLoaded', function() {
  const inputImagem = document.getElementById('edit_imagem');
  const preview = document.getElementById('edit-preview-imagem');
  
  if (inputImagem) {
    inputImagem.addEventListener('change', function() {
      const file = this.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
          preview.src = e.target.result;
          preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
      }
    });
  }
});

// ===============================
// Enviar edição
// ===============================
document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('form-editar-equipamento');
  
  if (form) {
    form.addEventListener('submit', function(e) {
      e.preventDefault();

      const formData = new FormData(this);
      const id = document.getElementById('edit_id').value;

      if (!id) {
        alert('ID do equipamento não encontrado');
        return;
      }
      
      

      fetch(`/editar-equipamento/${id}`, {
        method: 'POST',
        body: formData
      })
        .then(res => {
        if (!res.ok) throw new Error('Erro na requisição');
        return res.json();
      })
      .then(data => {
        alert(data.mensagem);
        fecharModalEditarEquipamento();
        location.reload();
      })
      .catch(err => {
        console.error(err);
        alert('Erro ao atualizar Equipamento');
      });
    });
  }
});
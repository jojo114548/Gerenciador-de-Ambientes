
//delete equipamento
function excluirEquipamento(id) {
    fetch(`/equipamentos/${id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.erro || 'Erro ao deletar equipamento');
            });
        }
        return response.json();
    })
    .then(data => {
      mostrarToast("equipamento deletado com sucesso!", "sucesso");
      setTimeout(() => location.reload(), 1200);
    })
    .catch(error => {
      console.error(err);
    mostrarToast("Erro de conexão", "erro");
    });
}

 
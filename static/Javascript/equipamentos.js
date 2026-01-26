
//delete equipamento
function excluir(id) {
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
        alert('equipamento deletado com sucesso!');
        window.location.reload();
    })
    .catch(error => {
        console.error(error);
        alert(error.message);
    });
}

 
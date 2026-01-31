                  



function excluirAmbiente(id) {
    if (!confirm('Deseja excluir este ambiente?')) return;

    fetch(`/ambientes/${id}/`, 
        { method: 'DELETE',
         credentials: 'include'
         })
        
        .then(r => {
            if (!r.ok) throw new Error();
            return r.json();
        })
        .then(() => {
            alert('Ambiente excluído com sucesso!');
            location.reload();
        })
        .catch(() => alert('Erro ao excluir ambiente'));
}


                  



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
            mostrarToast("Ambiente excluído com sucesso", "sucesso");
            location.reload();
        })
        .catch(() => mostrarToast("Erro ao excluir ambiente", "erro"));
      
}


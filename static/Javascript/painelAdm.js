function atualizarStatusAmbiente(pendenteId, status) {
    fetch(`/pendentes/${pendenteId}/status`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status })
    })
    .then(r => r.json())
    .then(() => location.reload());
}

function atualizarStatusEquipamento(pendenteId, status) {
    fetch(`/pendentes-equipamentos/${pendenteId}/status`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status })
    })
    .then(r => r.json())
    .then(() => location.reload());
}


function deletarUsuario(id) {
    if (!confirm("Deseja realmente excluir este usuário?")) return;

    fetch(`/usuarios/${id}`, {
        method: "DELETE"
    })
    .then(res => {
        if (!res.ok) throw new Error("Erro ao excluir usuário");
        return res.json();
    })
    .then(() => {
        alert("Usuário excluído com sucesso");
        window.location.reload();
    })
    .catch(err => {
        alert(err.message);
    });
}

function resetarSenhaPadrao(usuarioId) {
  if (!confirm("Deseja resetar a senha para o padrão (User + últimos 4 dígitos do CPF)?")) {
    return;
  }

  fetch(`/usuarios/${usuarioId}/senha`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({}) // 👈 envia vazio
  })
    .then(res => res.json())
    .then(res => {
      if (res.erro) return alert(res.erro);

      alert(res.mensagem || "Senha resetada com sucesso");
    })
    .catch(() => alert("Erro ao resetar senha"));
}

def test_listar_usuarios(client, monkeypatch):

    monkeypatch.setattr(
        "repository.usuario_repository.UsuarioRepository.listar",
        lambda: []
    )

    resp = client.get("/usuarios")

    assert resp.status_code == 200

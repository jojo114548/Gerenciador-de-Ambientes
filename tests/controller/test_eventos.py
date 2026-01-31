def test_listar_eventos(client, monkeypatch):

    monkeypatch.setattr(
        "repository.eventos_repository.EventosRepository.listar_eventos",
        lambda: []
    )

    monkeypatch.setattr(
        "repository.eventos_repository.EventosRepository.usuario_ja_inscrito",
        lambda *args, **kwargs: False
    )

    resp = client.get("/eventos")

    assert resp.status_code == 200

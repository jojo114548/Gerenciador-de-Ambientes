def test_listar_ambientes(client, monkeypatch):

    monkeypatch.setattr(
        "repository.ambiente_repository.AmbienteRepository.listar",
        lambda: []
    )

    resp = client.get("/ambientes")

    assert resp.status_code == 200

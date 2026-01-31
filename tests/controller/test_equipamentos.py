def test_listar_equipamentos(client, monkeypatch):

    monkeypatch.setattr(
        "repository.equipamento_repository.EquipamentoRepository.listar",
        lambda: []
    )

    resp = client.get("/equipamentos")

    assert resp.status_code == 200

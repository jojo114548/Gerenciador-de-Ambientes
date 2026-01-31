def test_criar_agendamento(client, monkeypatch):

    monkeypatch.setattr(
        "service.agendamento_service.AgendamentoService.criar",
        lambda *args, **kwargs: True
    )

    resp = client.post("/agendamentos", json={
        "ambiente_id": 1,
        "data": "2024-12-10",
        "hora_inicio": "10:00",
        "hora_fim": "12:00"
    })

    assert resp.status_code in (200, 201)

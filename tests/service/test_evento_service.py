from service.evento_service import EventoService


class FakeEventoRepo:
    @staticmethod
    def usuario_ja_inscrito(evento_id, usuario_id):
        return evento_id == 1


def test_marcar_inscricao_eventos():
    eventos = [
        {"id": 1, "nome": "Evento A"},
        {"id": 2, "nome": "Evento B"}
    ]

    resultado = EventoService.marcar_inscricao(
        eventos, "user-test-id", FakeEventoRepo
    )

    assert resultado[0]["inscrito"] is True
    assert resultado[1]["inscrito"] is False

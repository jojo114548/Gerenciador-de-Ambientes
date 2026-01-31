import pytest
from service.agendamento_service import AgendamentoService


class FakeAgendamentoRepo:
    @staticmethod
    def criar():
        return {"id": 10, "status": "criado"}


def test_criar_agendamento_sucesso():
    resultado = AgendamentoService.criar_agendamento(
        FakeAgendamentoRepo, ambiente_disponivel=True
    )

    assert resultado["status"] == "criado"


def test_criar_agendamento_ambiente_indisponivel():
    with pytest.raises(ValueError):
        AgendamentoService.criar_agendamento(
            FakeAgendamentoRepo, ambiente_disponivel=False
        )

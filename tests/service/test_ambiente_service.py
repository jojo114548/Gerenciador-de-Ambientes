import pytest
from service.ambiente_service import AmbienteService


class FakeAmbienteRepo:
    @staticmethod
    def listar():
        return [
            {"id": 1, "nome": "Sala 01"},
            {"id": 2, "nome": "Laboratório"}
        ]


class FakeAmbienteRepoErro:
    @staticmethod
    def listar():
        return None


def test_listar_ambientes_sucesso():
    ambientes = AmbienteService.listar_ambientes(FakeAmbienteRepo)

    assert len(ambientes) == 2
    assert ambientes[0]["nome"] == "Sala 01"


def test_listar_ambientes_erro():
    with pytest.raises(ValueError):
        AmbienteService.listar_ambientes(FakeAmbienteRepoErro)

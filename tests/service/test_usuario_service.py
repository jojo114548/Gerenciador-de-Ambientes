import pytest
from service.usuario_service import UsuarioService


def test_validar_usuario_sucesso():
    usuario = {"email": "teste@email.com", "senha": "123456"}
    assert UsuarioService.validar_usuario(usuario) is True


def test_validar_usuario_sem_email():
    with pytest.raises(ValueError):
        UsuarioService.validar_usuario({"senha": "123"})


def test_validar_usuario_sem_senha():
    with pytest.raises(ValueError):
        UsuarioService.validar_usuario({"email": "x@email.com"})

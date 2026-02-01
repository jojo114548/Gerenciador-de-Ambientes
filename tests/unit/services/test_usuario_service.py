# tests/unit/services/test_usuario_service.py
"""Testes para usuario_service - 8 testes"""
import pytest
from unittest.mock import patch, MagicMock


class TestUsuarioService:
    """Testes unitários do UsuarioService"""
    
    @patch('service.usuario_service.UsuarioRepository.listar')
    def test_listar_usuarios(self, mock_listar):
        """Deve listar todos os usuários"""
        from service.usuario_service import UsuarioService
        
        mock_listar.return_value = [
            {"id": 1, "name": "User 1"},
            {"id": 2, "name": "User 2"}
        ]
        
        resultado = UsuarioService.listar()
        
        assert len(resultado) == 2
        assert resultado[0]["name"] == "User 1"
        mock_listar.assert_called_once()
    
    @patch('service.usuario_service.bcrypt.hashpw')
    @patch('service.usuario_service.UsuarioRepository.adicionar')
    @patch('service.usuario_service.UsuarioRepository.buscar_por_email')
    def test_cadastrar_usuario_sucesso(self, mock_buscar, mock_adicionar, mock_hash):
        """Deve cadastrar novo usuário com sucesso"""
        from service.usuario_service import UsuarioService
        
        mock_buscar.return_value = None  # Email não existe
        mock_hash.return_value.decode.return_value = "hashed_password"
        
        dados = {
            "name": "Novo User",
            "email": "novo@teste.com",
            "senha": "senha123",
            "cpf": "12345678901",
            "role": "user",
            "status": "ativo",
            "data_nascimento": "1990-01-01"
        }
        
        resultado = UsuarioService.cadastrar(dados)
        
        assert resultado["email"] == "novo@teste.com"
        mock_adicionar.assert_called_once()
    
    @patch('service.usuario_service.UsuarioRepository.buscar_por_email')
    def test_cadastrar_usuario_email_existente(self, mock_buscar):
        """Deve lançar erro se email já existe"""
        from service.usuario_service import UsuarioService
        
        mock_buscar.return_value = {"id": 1, "email": "existe@teste.com"}
        
        dados = {
            "name": "Test",
            "email": "existe@teste.com",
            "senha": "senha123",
            "cpf": "12345678901",
            "role": "user",
            "status": "ativo",
            "data_nascimento": "1990-01-01"
        }
        
        with pytest.raises(ValueError, match="já está cadastrado"):
            UsuarioService.cadastrar(dados)
    
    def test_cadastrar_usuario_sem_campos_obrigatorios(self):
        """Deve lançar erro se faltam campos obrigatórios"""
        from service.usuario_service import UsuarioService
        
        dados = {"name": "Teste"}  # Faltando campos
        
        with pytest.raises(ValueError, match="obrigatório"):
            UsuarioService.cadastrar(dados)
    
    @patch('service.usuario_service.bcrypt.checkpw')
    @patch('service.usuario_service.UsuarioRepository.buscar_por_email')
    def test_autenticar_credenciais_validas(self, mock_buscar, mock_checkpw):
        """Deve autenticar com credenciais válidas"""
        from service.usuario_service import UsuarioService
        
        mock_buscar.return_value = {
            "id": 1,
            "email": "teste@teste.com",
            "senha": "$2b$12$hashedpassword"
        }
        mock_checkpw.return_value = True
        
        resultado = UsuarioService.autenticar("teste@teste.com", "senha123")
        
        assert resultado is not None
        assert resultado["id"] == 1
    
    @patch('service.usuario_service.UsuarioRepository.buscar_por_email')
    def test_autenticar_usuario_inexistente(self, mock_buscar):
        """Deve retornar None para usuário inexistente"""
        from service.usuario_service import UsuarioService
        
        mock_buscar.return_value = None
        
        resultado = UsuarioService.autenticar("naoexiste@teste.com", "senha")
        assert resultado is None
    
    @patch('service.usuario_service.bcrypt.checkpw')
    @patch('service.usuario_service.UsuarioRepository.buscar_por_email')
    def test_autenticar_senha_incorreta(self, mock_buscar, mock_checkpw):
        """Deve retornar None para senha incorreta"""
        from service.usuario_service import UsuarioService
        
        mock_buscar.return_value = {
            "id": 1,
            "senha": "$2b$12$hashedpassword"
        }
        mock_checkpw.return_value = False
        
        resultado = UsuarioService.autenticar("teste@teste.com", "senha_errada")
        assert resultado is None
    
    @patch('service.usuario_service.UsuarioRepository.deletar')
    def test_deletar_usuario(self, mock_deletar):
        """Deve deletar usuário"""
        from service.usuario_service import UsuarioService
        
        UsuarioService.deletar("user-id-123")
        mock_deletar.assert_called_once_with("user-id-123")


# Executar: pytest tests/unit/services/test_usuario_service.py -v
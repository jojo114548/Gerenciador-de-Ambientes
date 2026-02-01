import pytest
from unittest.mock import patch


class TestLoginController:
    """Testes de autenticação e login"""
    
    def test_home_renderiza_pagina_login(self, client):
        """GET / deve renderizar página de login"""
        resp = client.get("/")
        assert resp.status_code == 200
    
    @patch('controller.login_controller.UsuarioService.autenticar')
    @patch('controller.login_controller.create_access_token')
    def test_login_credenciais_validas(
        self, mock_token, mock_autenticar, client, mock_usuario
    ):
        """POST /login com credenciais válidas deve redirecionar"""
        mock_autenticar.return_value = mock_usuario
        mock_token.return_value = "fake-jwt-token"
        
        resp = client.post("/login", data={
            "email": "teste@nexus.com",
            "senha": "senha123"
        })
        
        assert resp.status_code in [200, 302]
        mock_autenticar.assert_called_once_with("teste@nexus.com", "senha123")
    
    @patch('controller.login_controller.UsuarioService.autenticar')
    def test_login_credenciais_invalidas(self, mock_autenticar, client):
        """POST /login com credenciais inválidas deve retornar 401"""
        mock_autenticar.return_value = None
        
        resp = client.post("/login", data={
            "email": "invalido@nexus.com",
            "senha": "senha_errada"
        })
        
        assert resp.status_code == 401
        assert b"inv" in resp.data.lower() or b"Email ou senha" in resp.data
    
    @patch('controller.login_controller.AmbientesService.listar')
    @patch('controller.login_controller.EquipamentoService.listar')
    @patch('controller.login_controller.UsuarioService.listar')
    @patch('controller.login_controller.EventosRepository.listar')
    @patch('controller.login_controller.EventosRepository.usuario_ja_inscrito')
    def test_index_usuario_logado(
        self, mock_inscrito, mock_eventos, mock_usuarios,
        mock_equip, mock_amb, client_autenticado
    ):
        """GET /index com usuário logado deve renderizar página principal"""
        mock_amb.return_value = []
        mock_equip.return_value = []
        mock_usuarios.return_value = []
        mock_eventos.return_value = []
        mock_inscrito.return_value = False
        
        resp = client_autenticado.get("/index")
        assert resp.status_code == 200
    
    def test_index_sem_autenticacao_redireciona(self, client):
        """GET /index sem autenticação deve retornar 401 ou redirecionar"""
        resp = client.get("/index")
        assert resp.status_code in [302, 401]
    
    def test_logout_usuario_logado(self, client_autenticado):
        """GET /logout deve deslogar usuário e redirecionar"""
        resp = client_autenticado.get("/logout")
        assert resp.status_code in [200, 302]
    
    def test_logout_sem_autenticacao(self, client):
        """GET /logout sem autenticação deve retornar 401"""
        resp = client.get("/logout")
        assert resp.status_code in [302, 401]
    
    @patch('controller.login_controller.UsuarioRepository.buscar_por_email')
    @patch('controller.login_controller.bcrypt.hashpw')
    @patch('controller.login_controller.UsuarioRepository.adicionar')
    def test_garantir_admin_padrao_cria_admin(
        self, mock_add, mock_hash, mock_buscar
    ):
        """garantir_admin_padrao deve criar admin se não existir"""
        from controller.login_controller import garantir_admin_padrao
        
        mock_buscar.return_value = None  # Admin não existe
        mock_hash.return_value.decode.return_value = "hashed_password"
        
        garantir_admin_padrao()
        
        mock_buscar.assert_called_once_with("admin@nexus.com")
        mock_add.assert_called_once()


# Executar: pytest tests/integration/controllers/test_login_controller.py -v

"""
Testes para login_controller - 8 testes = ~7% de cobertura
PRIORIDADE: ALTA
"""
import pytest
from unittest.mock import patch


class TestLoginController:
    """Testes de autenticação e login"""
    
    def test_home_renderiza_pagina_login(self, client):
        """GET / deve renderizar página de login"""
        resp = client.get("/")
        assert resp.status_code == 200
    
    @patch('controller.login_controller.UsuarioService.autenticar')
    @patch('controller.login_controller.create_access_token')
    def test_login_credenciais_validas(
        self, mock_token, mock_autenticar, client, mock_usuario
    ):
        """POST /login com credenciais válidas deve redirecionar"""
        mock_autenticar.return_value = mock_usuario
        mock_token.return_value = "fake-jwt-token"
        
        resp = client.post("/login", data={
            "email": "teste@nexus.com",
            "senha": "senha123"
        })
        
        assert resp.status_code in [200, 302]
        mock_autenticar.assert_called_once_with("teste@nexus.com", "senha123")
    
    @patch('controller.login_controller.UsuarioService.autenticar')
    def test_login_credenciais_invalidas(self, mock_autenticar, client):
        """POST /login com credenciais inválidas deve retornar 401"""
        mock_autenticar.return_value = None
        
        resp = client.post("/login", data={
            "email": "invalido@nexus.com",
            "senha": "senha_errada"
        })
        
        assert resp.status_code == 401
        assert b"inv" in resp.data.lower() or b"Email ou senha" in resp.data
    
    @patch('controller.login_controller.AmbientesService.listar')
    @patch('controller.login_controller.EquipamentoService.listar')
    @patch('controller.login_controller.UsuarioService.listar')
    @patch('controller.login_controller.EventosRepository.listar')
    @patch('controller.login_controller.EventosRepository.usuario_ja_inscrito')
    def test_index_usuario_logado(
        self, mock_inscrito, mock_eventos, mock_usuarios,
        mock_equip, mock_amb, client_autenticado
    ):
        """GET /index com usuário logado deve renderizar página principal"""
        mock_amb.return_value = []
        mock_equip.return_value = []
        mock_usuarios.return_value = []
        mock_eventos.return_value = []
        mock_inscrito.return_value = False
        
        resp = client_autenticado.get("/index")
        assert resp.status_code == 200
    
    def test_index_sem_autenticacao_redireciona(self, client):
        """GET /index sem autenticação deve retornar 401 ou redirecionar"""
        resp = client.get("/index")
        assert resp.status_code in [302, 401]
    
    def test_logout_usuario_logado(self, client_autenticado):
        """GET /logout deve deslogar usuário e redirecionar"""
        resp = client_autenticado.get("/logout")
        assert resp.status_code in [200, 302]
    
    def test_logout_sem_autenticacao(self, client):
        """GET /logout sem autenticação deve retornar 401"""
        resp = client.get("/logout")
        assert resp.status_code in [302, 401]
    
    @patch('controller.login_controller.UsuarioRepository.buscar_por_email')
    @patch('controller.login_controller.bcrypt.hashpw')
    @patch('controller.login_controller.UsuarioRepository.adicionar')
    def test_garantir_admin_padrao_cria_admin(
        self, mock_add, mock_hash, mock_buscar
    ):
        """garantir_admin_padrao deve criar admin se não existir"""
        from controller.login_controller import garantir_admin_padrao
        
        mock_buscar.return_value = None  # Admin não existe
        mock_hash.return_value.decode.return_value = "hashed_password"
        
        garantir_admin_padrao()
        
        mock_buscar.assert_called_once_with("admin@nexus.com")
        mock_add.assert_called_once()

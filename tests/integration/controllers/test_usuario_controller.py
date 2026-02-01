"""
Testes para usuario_controller.py
Cobertura: ~9% do total
Total de testes: 10
"""

import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO


class TestUsuarioController:
    """Testes de CRUD de usuários"""
    
    @patch('controller.usuario_controller.UsuarioService.atualizar')
    def test_editar_usuario_proprio_sucesso(self, mock_atualizar, client_autenticado):
        """PUT /usuarios/user-123 pelo próprio usuário deve atualizar"""
        mock_atualizar.return_value = True
        
        dados = {
            'name': 'Usuario Atualizado',
            'email': 'novo@teste.com',
            'cpf': '12345678901',
            'telefone': '11999999999'
        }
        
        response = client_autenticado.put('/usuarios/user-123',
                                         data=dados,
                                         content_type='multipart/form-data')
        
        assert response.status_code == 200
        assert b"atualizado com sucesso" in response.data.lower()
        mock_atualizar.assert_called_once()
    
    @patch('controller.usuario_controller.UsuarioService.atualizar')
    def test_editar_usuario_admin_sucesso(self, mock_atualizar, client_admin):
        """PUT /usuarios/user-123 por admin deve atualizar qualquer usuário"""
        mock_atualizar.return_value = True
        
        dados = {
            'name': 'Usuario Modificado',
            'email': 'modificado@teste.com'
        }
        
        response = client_admin.put('/usuarios/user-123',
                                   data=dados,
                                   content_type='multipart/form-data')
        
        assert response.status_code == 200
        mock_atualizar.assert_called_once()
    
    def test_editar_usuario_outro_sem_permissao(self, client_autenticado):
        """PUT /usuarios/outro-user sem admin deve retornar 403"""
        dados = {
            'name': 'Tentativa Hack',
            'email': 'hack@teste.com'
        }
        
        response = client_autenticado.put('/usuarios/outro-user-id',
                                         data=dados,
                                         content_type='multipart/form-data')
        
        assert response.status_code == 403
        assert b"permiss" in response.data.lower()
    
    @patch('controller.usuario_controller.UsuarioService.atualizar')
    def test_editar_usuario_sem_campos_obrigatorios(self, mock_atualizar, 
                                                     client_autenticado):
        """PUT /usuarios/user-123 sem name/email deve retornar 400"""
        dados = {
            'telefone': '11999999999'
            # Faltando name e email
        }
        
        response = client_autenticado.put('/usuarios/user-123',
                                         data=dados,
                                         content_type='multipart/form-data')
        
        assert response.status_code == 400
        assert b"obrigat" in response.data.lower()
    
    @patch('controller.usuario_controller.UsuarioService.alterar_senha')
    def test_alterar_senha_proprio_sucesso(self, mock_alterar, client_autenticado):
        """PUT /usuarios/user-123/senha pelo próprio deve alterar senha"""
        mock_alterar.return_value = True
        
        dados = {
            'senha_atual': 'senha123',
            'senha_nova': 'NovaSenha@123'
        }
        
        response = client_autenticado.put('/usuarios/user-123/senha',
                                         json=dados)
        
        assert response.status_code == 200
        assert b"Senha alterada com sucesso" in response.data
        mock_alterar.assert_called_once()
    
    @patch('controller.usuario_controller.UsuarioService.resetar_senha_padrao')
    def test_resetar_senha_admin(self, mock_resetar, client_admin):
        """PUT /usuarios/user-123/senha por admin deve resetar senha"""
        mock_resetar.return_value = True
        
        dados = {
            'senha_nova': 'NovaSenha@123'
        }
        
        response = client_admin.put('/usuarios/user-123/senha',
                                   json=dados)
        
        assert response.status_code == 200
        assert b"resetada" in response.data.lower()
        mock_resetar.assert_called_once()
    
    def test_alterar_senha_proprio_sem_senha_atual(self, client_autenticado):
        """PUT /usuarios/user-123/senha sem senha_atual deve retornar 400"""
        dados = {
            'senha_nova': 'NovaSenha@123'
            # Faltando senha_atual
        }
        
        response = client_autenticado.put('/usuarios/user-123/senha',
                                         json=dados)
        
        assert response.status_code == 400
        assert b"obrigat" in response.data.lower()
    
    @patch('controller.usuario_controller.UsuarioService.deletar')
    def test_deletar_usuario_proprio_sucesso(self, mock_deletar, client_autenticado):
        """DELETE /usuarios/user-123 pelo próprio deve deletar conta"""
        mock_deletar.return_value = True
        
        response = client_autenticado.delete('/usuarios/user-123')
        
        assert response.status_code == 200
        assert b"exclu" in response.data.lower()
        mock_deletar.assert_called_once_with('user-123')
    
    @patch('controller.usuario_controller.UsuarioService.deletar')
    def test_deletar_usuario_admin_sucesso(self, mock_deletar, client_admin):
        """DELETE /usuarios/user-123 por admin deve deletar usuário"""
        mock_deletar.return_value = True
        
        response = client_admin.delete('/usuarios/user-123')
        
        assert response.status_code == 200
        assert b"removido" in response.data.lower()
        mock_deletar.assert_called_once()
    
    @patch('controller.usuario_controller.UsuarioService.cadastrar')
    def test_novo_usuario_admin_sucesso(self, mock_cadastrar, client_admin):
        """POST /novo-usuario por admin deve criar usuário"""
        mock_cadastrar.return_value = {
            'id': 'new-user-123',
            'name': 'Novo Usuario',
            'email': 'novo@teste.com'
        }
        
        dados = {
            'name': 'Novo Usuario',
            'email': 'novo@teste.com',
            'cpf': '12345678901',
            'senha': 'Senha@123',
            'role': 'user',
            'status': 'ativo',
            'data_nascimento': '1995-05-15'
        }
        
        response = client_admin.post('/novo-usuario',
                                    data=dados,
                                    content_type='multipart/form-data')
        
        assert response.status_code == 201
        assert b"cadastrado com sucesso" in response.data.lower()
        mock_cadastrar.assert_called_once()
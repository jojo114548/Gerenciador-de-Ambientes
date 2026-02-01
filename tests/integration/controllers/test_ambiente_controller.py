# tests/integration/controllers/test_ambiente_controller.py
"""Testes para ambiente_controller - 9 testes"""
import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO


class TestAmbienteController:
    """Testes de CRUD de ambientes"""
    
    @patch('controller.ambiente_controller.UsuarioService.listar')
    @patch('controller.ambiente_controller.AmbientesService.listar')
    def test_listar_ambientes(self, mock_amb, mock_users, client_autenticado):
        """GET /ambientes deve listar ambientes"""
        mock_amb.return_value = [{"id": 1, "name": "Sala A"}]
        mock_users.return_value = []
        
        resp = client_autenticado.get("/ambientes")
        assert resp.status_code == 200
        mock_amb.assert_called_once()
    
    @patch('controller.ambiente_controller.AmbientesService.inserir_ambiente')
    @patch('os.makedirs')
    def test_criar_ambiente_admin(self, mock_mk, mock_inserir, client_admin):
        """POST /novo-ambiente com admin cria ambiente"""
        mock_inserir.return_value = 1
        
        dados = {
            'name': 'Nova Sala',
            'type': 'sala',
            'capacidade': 20,
            'status': 'Disponivel',
            'descricao': 'Sala teste',
            'localizacao': '1º andar',
            'area': '30m²',
            'recursos[]': ['TV', 'Projetor']
        }
        
        resp = client_admin.post('/novo-ambiente', data=dados)
        assert resp.status_code == 201
        mock_inserir.assert_called_once()
    
    def test_criar_ambiente_sem_permissao(self, client_autenticado):
        """POST /novo-ambiente sem admin retorna 403"""
        resp = client_autenticado.post('/novo-ambiente', data={
            'name': 'Teste'
        })
        assert resp.status_code == 403
    
    @patch('controller.ambiente_controller.AmbientesService.atualizar_ambiente')
    def test_atualizar_ambiente_admin(self, mock_atualizar, client_admin):
        """POST /ambientes/1 atualiza ambiente"""
        mock_atualizar.return_value = True
        
        dados = {
            'name': 'Sala Atualizada',
            'capacidade': 25,
            'image_atual': '/static/imgs/sala.jpg',
            'recursos[]': ['TV']
        }
        
        resp = client_admin.post('/ambientes/1', data=dados)
        assert resp.status_code == 200
        mock_atualizar.assert_called_once()
    
    def test_atualizar_ambiente_sem_permissao(self, client_autenticado):
        """POST /ambientes/1 sem admin retorna 403"""
        resp = client_autenticado.post('/ambientes/1', data={'name': 'Teste'})
        assert resp.status_code == 403
    
    @patch('controller.ambiente_controller.AmbientesService.deletar_ambiente')
    def test_deletar_ambiente_admin(self, mock_deletar, client_admin):
        """DELETE /ambientes/1/ deleta ambiente"""
        mock_deletar.return_value = True
        
        resp = client_admin.delete('/ambientes/1/')
        assert resp.status_code == 200
        mock_deletar.assert_called_once_with('1')
    
    def test_deletar_ambiente_sem_permissao(self, client_autenticado):
        """DELETE /ambientes/1/ sem admin retorna 403"""
        resp = client_autenticado.delete('/ambientes/1/')
        assert resp.status_code == 403
    
    @patch('controller.ambiente_controller.AmbientesService.inserir_ambiente')
    def test_criar_ambiente_erro_validacao(self, mock_inserir, client_admin):
        """POST /novo-ambiente com dados inválidos retorna 400"""
        mock_inserir.side_effect = ValueError("Dados inválidos")
        
        dados = {'name': 'Teste', 'capacidade': -5}
        resp = client_admin.post('/novo-ambiente', data=dados)
        assert resp.status_code == 400
    
    @patch('controller.ambiente_controller.AmbientesService.atualizar_ambiente')
    @patch('os.makedirs')
    def test_atualizar_ambiente_com_imagem(self, mock_mk, mock_atualizar, client_admin):
        """POST /ambientes/1 com upload de imagem"""
        mock_atualizar.return_value = True
        
        dados = {
            'name': 'Sala',
            'capacidade': 20,
            'image': (BytesIO(b'fake image'), 'sala.jpg'),
            'recursos[]': []
        }
        
        resp = client_admin.post('/ambientes/1', 
                                data=dados,
                                content_type='multipart/form-data')
        assert resp.status_code == 200


# Executar: pytest tests/integration/controllers/test_ambiente_controller.py -v
"""
Testes para equipamento_controller.py
Cobertura: ~8% do total
Total de testes: 9
"""

import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO


class TestEquipamentoController:
    """Testes de CRUD de equipamentos"""
    
    @patch('controller.equipamento_controller.UsuarioService.listar')
    @patch('controller.equipamento_controller.EquipamentoService.listar')
    def test_listar_equipamentos(self, mock_equip_listar, mock_users_listar,
                                 client_autenticado, mock_lista_equipamentos, 
                                 mock_lista_usuarios):
        """GET /equipamentos deve listar equipamentos com sucesso"""
        mock_equip_listar.return_value = mock_lista_equipamentos
        mock_users_listar.return_value = mock_lista_usuarios
        
        response = client_autenticado.get("/equipamentos")
        
        assert response.status_code == 200
        mock_equip_listar.assert_called_once()
        mock_users_listar.assert_called_once()
    
    @patch('controller.equipamento_controller.EquipamentoService.inserir_equipamento')
    def test_cadastrar_equipamento_admin_sucesso(self, mock_inserir, client_admin):
        """POST /equipamento com admin deve criar equipamento"""
        mock_inserir.return_value = 1
        
        dados = {
            'name': 'Projetor Epson',
            'categoria': 'audio_video',
            'status': 'Disponivel',
            'descricao': 'Projetor Full HD',
            'marca': 'Epson',
            'modelo': 'X500',
            'condicao': 'Novo',
            'quantidade_disponivel': 5,
            'image_atual': '/static/imgs/projetor.jpg',
            'especificacoes[]': ['Full HD', 'HDMI', '3000 lumens']
        }
        
        response = client_admin.post('/equipamento', data=dados)
        
        assert response.status_code == 200
        assert b"Equipamento cadastrado com sucesso" in response.data
        mock_inserir.assert_called_once()
    
    def test_cadastrar_equipamento_sem_permissao(self, client_autenticado):
        """POST /equipamento sem admin deve retornar 403"""
        dados = {
            'name': 'Teste Equipamento',
            'categoria': 'informatica'
        }
        
        response = client_autenticado.post('/equipamento', data=dados)
        
        assert response.status_code == 403
        assert b"permiss" in response.data.lower()
    
    @patch('controller.equipamento_controller.EquipamentoService.atualizar_equipamento')
    def test_editar_equipamento_admin_sucesso(self, mock_atualizar, client_admin):
        """POST /editar-equipamento/1 com admin deve atualizar equipamento"""
        mock_atualizar.return_value = True
        
        dados = {
            'name': 'Projetor Atualizado',
            'categoria': 'audio_video',
            'status': 'Disponivel',
            'descricao': 'Projetor 4K',
            'marca': 'Epson',
            'modelo': 'X600',
            'condicao': 'Novo',
            'quantidade_disponivel': 3,
            'image_atual': '/static/imgs/projetor.jpg',
            'especificacoes[]': ['4K', 'HDMI']
        }
        
        response = client_admin.post('/editar-equipamento/1', data=dados)
        
        assert response.status_code == 200
        assert b"Equipamento atualizado com sucesso" in response.data
        mock_atualizar.assert_called_once()
    
    def test_editar_equipamento_sem_permissao(self, client_autenticado):
        """POST /editar-equipamento/1 sem admin deve retornar 403"""
        dados = {
            'name': 'Tentativa Atualização',
            'quantidade_disponivel': 5
        }
        
        response = client_autenticado.post('/editar-equipamento/1', data=dados)
        
        assert response.status_code == 403
        assert b"permiss" in response.data.lower()
    
    @patch('controller.equipamento_controller.EquipamentoService.deletar_equipamento')
    def test_deletar_equipamento_admin_sucesso(self, mock_deletar, client_admin):
        """DELETE /equipamentos/1 com admin deve deletar equipamento"""
        mock_deletar.return_value = True
        
        response = client_admin.delete('/equipamentos/1')
        
        assert response.status_code == 200
        assert b"exclu" in response.data.lower()
        mock_deletar.assert_called_once_with('1')
    
    def test_deletar_equipamento_sem_permissao(self, client_autenticado):
        """DELETE /equipamentos/1 sem admin deve retornar 403"""
        response = client_autenticado.delete('/equipamentos/1')
        
        assert response.status_code == 403
        assert b"permiss" in response.data.lower()
    
    @patch('controller.equipamento_controller.EquipamentoService.atualizar_equipamento')
    def test_editar_equipamento_sem_quantidade(self, mock_atualizar, client_admin):
        """POST /editar-equipamento/1 sem quantidade deve retornar 400"""
        dados = {
            'name': 'Projetor',
            'categoria': 'audio_video',
            'quantidade_disponivel': ''  # Vazio - inválido
        }
        
        response = client_admin.post('/editar-equipamento/1', data=dados)
        
        assert response.status_code == 400
        assert b"obrigat" in response.data.lower()
    
    @patch('controller.equipamento_controller.EquipamentoService.inserir_equipamento')
    @patch('os.makedirs')
    def test_cadastrar_equipamento_com_imagem(self, mock_makedirs, mock_inserir,
                                              client_admin):
        """POST /equipamento com upload de imagem deve salvar arquivo"""
        mock_inserir.return_value = 1
        
        dados = {
            'name': 'Notebook Dell',
            'categoria': 'informatica',
            'status': 'Disponivel',
            'descricao': 'Notebook i7',
            'marca': 'Dell',
            'modelo': 'Inspiron',
            'condicao': 'Novo',
            'quantidade_disponivel': 10,
            'image': (BytesIO(b'fake image data'), 'notebook.jpg'),
            'especificacoes[]': ['i7', '16GB RAM']
        }
        
        response = client_admin.post('/equipamento',
                                    data=dados,
                                    content_type='multipart/form-data')
        
        assert response.status_code == 200
        mock_inserir.assert_called_once()
"""
Testes para evento_controller.py
Cobertura: ~7% do total
Total de testes: 8
"""

import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO


class TestEventoController:
    """Testes de CRUD de eventos"""
    
    @patch('controller.evento_controller.RecursosRepository.listar_equipamentos')
    @patch('controller.evento_controller.RecursosRepository.listar_ambientes')
    @patch('controller.evento_controller.UsuarioService.listar')
    @patch('controller.evento_controller.EventosRepository.listar')
    @patch('controller.evento_controller.EventosRepository.usuario_ja_inscrito')
    def test_listar_eventos(self, mock_inscrito, mock_listar, mock_users,
                           mock_amb, mock_equip, client_autenticado,
                           mock_evento, mock_lista_usuarios):
        """GET /eventos deve listar eventos com status de inscrição"""
        mock_listar.return_value = [mock_evento]
        mock_inscrito.return_value = False
        mock_users.return_value = mock_lista_usuarios
        mock_amb.return_value = []
        mock_equip.return_value = []
        
        response = client_autenticado.get("/eventos")
        
        assert response.status_code == 200
        mock_listar.assert_called_once()
        mock_inscrito.assert_called_once()
    
    @patch('controller.evento_controller.EventosService.criar')
    @patch('controller.evento_controller.NotificacaoService.criar_notificacao')
    def test_criar_evento_sucesso(self, mock_notif, mock_criar, client_autenticado):
        """POST /eventos deve criar evento com sucesso"""
        mock_criar.return_value = 1
        
        dados = {
            'titulo': 'Workshop Python',
            'data_evento': '2026-02-15',
            'hora_evento': '14:00',
            'ambiente_id': '1',
            'localizacao': 'Sala A',
            'descricao': 'Workshop de Python básico',
            'participantes': '0',
            'capacidade': '30',
            'instrutor': 'Prof. João',
            'tipo': 'workshop',
            'equipamentos[]': ['1', '2'],
            'quantidades[]': ['2', '1']
        }
        
        response = client_autenticado.post('/eventos', data=dados)
        
        assert response.status_code == 201
        assert b"Evento criado com sucesso" in response.data
        mock_criar.assert_called_once()
        mock_notif.assert_called_once()
    
    @patch('controller.evento_controller.EventosService.criar')
    def test_criar_evento_erro_validacao(self, mock_criar, client_autenticado):
        """POST /eventos com dados inválidos deve retornar 400"""
        mock_criar.side_effect = ValueError("Campo obrigatório ausente: titulo")
        
        dados = {
            'data_evento': '2026-02-15',
            # Faltando campos obrigatórios
        }
        
        response = client_autenticado.post('/eventos', data=dados)
        
        assert response.status_code == 400
        assert b"erro" in response.data.lower()
    
    @patch('controller.evento_controller.EventosService.remover')
    def test_deletar_evento_admin_sucesso(self, mock_remover, client_admin):
        """DELETE /eventos/1 com admin deve deletar evento"""
        mock_remover.return_value = True
        
        response = client_admin.delete('/eventos/1')
        
        assert response.status_code == 200
        assert b"exclu" in response.data.lower()
        mock_remover.assert_called_once_with('1')
    
    def test_deletar_evento_sem_permissao(self, client_autenticado):
        """DELETE /eventos/1 sem admin deve retornar 403"""
        response = client_autenticado.delete('/eventos/1')
        
        assert response.status_code == 403
        assert b"permiss" in response.data.lower()
    
    @patch('controller.evento_controller.EventosService.inscrever')
    def test_inscrever_evento_sucesso(self, mock_inscrever, client_autenticado):
        """POST /eventos/1/inscrever deve inscrever usuário"""
        mock_inscrever.return_value = True
        
        response = client_autenticado.post('/eventos/1/inscrever')
        
        assert response.status_code == 200
        assert b"realizada" in response.data.lower()
        mock_inscrever.assert_called_once()
    
    @patch('controller.evento_controller.EventosService.inscrever')
    def test_inscrever_evento_ja_inscrito(self, mock_inscrever, client_autenticado):
        """POST /eventos/1/inscrever quando já inscrito deve retornar 400"""
        mock_inscrever.side_effect = ValueError("Usuário já inscrito")
        
        response = client_autenticado.post('/eventos/1/inscrever')
        
        assert response.status_code == 400
        assert b"erro" in response.data.lower()
    
    @patch('controller.evento_controller.EventosService.buscar_detalhes')
    def test_detalhes_evento_sucesso(self, mock_detalhes, client_autenticado,
                                     mock_evento):
        """GET /eventos/1/detalhes deve retornar detalhes do evento"""
        mock_detalhes.return_value = mock_evento
        
        response = client_autenticado.get('/eventos/1/detalhes')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['titulo'] == 'Workshop de Python'
        mock_detalhes.assert_called_once_with('1')
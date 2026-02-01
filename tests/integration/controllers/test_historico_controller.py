"""
Testes para historico_controller.py
Cobertura: ~2% do total
Total de testes: 3
"""

import pytest
from unittest.mock import patch, MagicMock


class TestHistoricoController:
    """Testes de histórico de agendamentos"""
    
    @patch('controller.historico_controller.UsuarioService.listar')
    @patch('controller.historico_controller.HistoricoRepository.listar_todos')
    @patch('controller.historico_controller.HistoricoEquipamentoRepository.listar')
    @patch('controller.historico_controller.HistoricoService.atualizar_concluidos')
    @patch('controller.historico_controller.HistoricoEquipamentoService.atualizar_concluidos')
    def test_listar_historico(self, mock_equip_atualizar, mock_amb_atualizar,
                             mock_equip_listar, mock_amb_listar, mock_users,
                             client_autenticado, mock_lista_usuarios):
        """GET /historico deve listar históricos de ambientes e equipamentos"""
        mock_equip_atualizar.return_value = None
        mock_amb_atualizar.return_value = None
        mock_equip_listar.return_value = []
        mock_amb_listar.return_value = []
        mock_users.return_value = mock_lista_usuarios
        
        response = client_autenticado.get("/historico")
        
        assert response.status_code == 200
        mock_equip_atualizar.assert_called_once()
        mock_amb_atualizar.assert_called_once()
        mock_equip_listar.assert_called_once()
        mock_amb_listar.assert_called_once()
    
    @patch('controller.historico_controller.HistoricoService.cancelar_historico')
    def test_cancelar_historico_ambiente_sucesso(self, mock_cancelar,
                                                 client_autenticado):
        """POST /historico/cancelar/1 deve cancelar histórico de ambiente"""
        mock_cancelar.return_value = True
        
        response = client_autenticado.post('/historico/cancelar/1')
        
        assert response.status_code == 200
        assert b"cancelado com sucesso" in response.data.lower()
        mock_cancelar.assert_called_once_with(1, 'user-123')
    
    @patch('controller.historico_controller.HistoricoEquipamentoService.cancelar_historico')
    def test_cancelar_historico_equipamento_sucesso(self, mock_cancelar,
                                                    client_autenticado):
        """POST /historico_equipamentos/cancelar/1 deve cancelar histórico de equipamento"""
        mock_cancelar.return_value = True
        
        response = client_autenticado.post('/historico_equipamentos/cancelar/1')
        
        assert response.status_code == 200
        assert b"cancelado com sucesso" in response.data.lower()
        mock_cancelar.assert_called_once_with(1, 'user-123')
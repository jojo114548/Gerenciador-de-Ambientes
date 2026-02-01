"""
Testes para pendente_controller.py
Cobertura: ~3% do total
Total de testes: 4
"""

import pytest
from unittest.mock import patch, MagicMock


class TestPendenteController:
    """Testes de atualização de status de pendentes"""
    
    @patch('controller.pendente_controller.PendenteService.atualizar_status')
    def test_atualizar_status_pendente_ambiente_sucesso(self, mock_atualizar,
                                                        client_autenticado):
        """POST /pendentes/1/status deve atualizar status de pendente de ambiente"""
        mock_atualizar.return_value = {
            'id': 1,
            'status': 'Confirmado'
        }
        
        dados = {
            'status': 'Confirmado'
        }
        
        response = client_autenticado.post('/pendentes/1/status',
                                          json=dados)
        
        assert response.status_code == 200
        assert b"Status atualizado com sucesso" in response.data
        mock_atualizar.assert_called_once_with(1, 'Confirmado')
    
    @patch('controller.pendente_controller.PendenteService.atualizar_status')
    def test_atualizar_status_pendente_ambiente_erro(self, mock_atualizar,
                                                     client_autenticado):
        """POST /pendentes/1/status com erro deve retornar 400"""
        mock_atualizar.side_effect = ValueError("Pendente não encontrado")
        
        dados = {
            'status': 'Confirmado'
        }
        
        response = client_autenticado.post('/pendentes/1/status',
                                          json=dados)
        
        assert response.status_code == 400
        assert b"erro" in response.data.lower()
    
    @patch('controller.pendente_controller.PendenteServiceEquip.atualizar_status')
    def test_atualizar_status_pendente_equipamento_sucesso(self, mock_atualizar,
                                                           client_autenticado):
        """PUT /pendentes-equipamentos/1/status deve atualizar status de equipamento"""
        mock_atualizar.return_value = {
            'id': 1,
            'status': 'Confirmado'
        }
        
        dados = {
            'status': 'Confirmado'
        }
        
        response = client_autenticado.put('/pendentes-equipamentos/1/status',
                                         json=dados)
        
        assert response.status_code == 200
        assert b"equipamento atualizado com sucesso" in response.data.lower()
        mock_atualizar.assert_called_once_with(1, 'Confirmado')
    
    @patch('controller.pendente_controller.PendenteServiceEquip.atualizar_status')
    def test_atualizar_status_pendente_equipamento_erro(self, mock_atualizar,
                                                        client_autenticado):
        """PUT /pendentes-equipamentos/1/status com erro deve retornar 400"""
        mock_atualizar.side_effect = ValueError("Equipamento não disponível")
        
        dados = {
            'status': 'Confirmado'
        }
        
        response = client_autenticado.put('/pendentes-equipamentos/1/status',
                                         json=dados)
        
        assert response.status_code == 400
        assert b"erro" in response.data.lower()
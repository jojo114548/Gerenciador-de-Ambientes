"""
Testes para agendamento_controller.py
Cobertura: ~5% do total
Total de testes: 6
"""

import pytest
from unittest.mock import patch, MagicMock


class TestAgendamentoController:
    """Testes de criação de agendamentos"""
    
    @patch('controller.agendamento_controller.NotificacaoService.criar_notificacao')
    @patch('controller.agendamento_controller.PendenteService.criar_pendente')
    @patch('controller.agendamento_controller.AgendamentosService.criar_agendamento')
    @patch('controller.agendamento_controller.AgendamentosRepository.existe_conflito')
    def test_criar_agendamento_ambiente_sucesso(self, mock_conflito, mock_criar,
                                                mock_pendente, mock_notif,
                                                client_autenticado):
        """POST /agendamentos deve criar agendamento de ambiente"""
        mock_conflito.return_value = False
        mock_criar.return_value = 1
        mock_pendente.return_value = 1
        
        dados = {
            'ambiente_id': 1,
            'data': '2026-02-20',
            'hora_inicio': '09:00',
            'hora_fim': '11:00',
            'finalidade': 'Reunião de equipe'
        }
        
        response = client_autenticado.post('/agendamentos',
                                          json=dados)
        
        assert response.status_code == 201
        assert b"enviado para aprovac" in response.data.lower()
        mock_criar.assert_called_once()
        mock_pendente.assert_called_once()
        mock_notif.assert_called_once()
    
    @patch('controller.agendamento_controller.AgendamentosRepository.existe_conflito')
    def test_criar_agendamento_ambiente_conflito(self, mock_conflito, 
                                                 client_autenticado):
        """POST /agendamentos com conflito deve retornar 409"""
        mock_conflito.return_value = True
        
        dados = {
            'ambiente_id': 1,
            'data': '2026-02-20',
            'hora_inicio': '09:00',
            'hora_fim': '11:00',
            'finalidade': 'Reunião'
        }
        
        response = client_autenticado.post('/agendamentos',
                                          json=dados)
        
        assert response.status_code == 409
        assert b"conflito" in response.data.lower() or b"existe" in response.data.lower()
    
    @patch('controller.agendamento_controller.NotificacaoService.criar_notificacao')
    @patch('controller.agendamento_controller.PendenteServiceEquip.criar_pendente')
    @patch('controller.agendamento_controller.AgendamentoEquipamentoService.criar_agendamento')
    @patch('controller.agendamento_controller.AgendamentoEquipamentoRepository.existe_conflito')
    def test_criar_agendamento_equipamento_sucesso(self, mock_conflito, mock_criar,
                                                   mock_pendente, mock_notif,
                                                   client_autenticado):
        """POST /agendamentos_equipamentos deve criar agendamento de equipamento"""
        mock_conflito.return_value = False
        mock_criar.return_value = 1
        mock_pendente.return_value = 1
        
        dados = {
            'equipamento_id': 1,
            'data': '2026-02-21',
            'hora_inicio': '10:00',
            'hora_fim': '12:00',
            'finalidade': 'Apresentação'
        }
        
        response = client_autenticado.post('/agendamentos_equipamentos',
                                          json=dados)
        
        assert response.status_code == 201
        assert b"equipamento enviado para aprovac" in response.data.lower()
        mock_criar.assert_called_once()
        mock_pendente.assert_called_once()
        mock_notif.assert_called_once()
    
    @patch('controller.agendamento_controller.AgendamentoEquipamentoRepository.existe_conflito')
    def test_criar_agendamento_equipamento_conflito(self, mock_conflito,
                                                    client_autenticado):
        """POST /agendamentos_equipamentos com conflito deve retornar 409"""
        mock_conflito.return_value = True
        
        dados = {
            'equipamento_id': 1,
            'data': '2026-02-21',
            'hora_inicio': '10:00',
            'hora_fim': '12:00',
            'finalidade': 'Teste'
        }
        
        response = client_autenticado.post('/agendamentos_equipamentos',
                                          json=dados)
        
        assert response.status_code == 409
        assert b"conflito" in response.data.lower() or b"existe" in response.data.lower()
    
    def test_criar_agendamento_equipamento_sem_dados_obrigatorios(self, 
                                                                  client_autenticado):
        """POST /agendamentos_equipamentos sem data/finalidade deve retornar 400"""
        dados = {
            'equipamento_id': 1,
            'hora_inicio': '10:00'
            # Faltando data e finalidade
        }
        
        response = client_autenticado.post('/agendamentos_equipamentos',
                                          json=dados)
        
        assert response.status_code == 400
        assert b"obrigat" in response.data.lower()
    
    @patch('controller.agendamento_controller.AgendamentosService.criar_agendamento')
    @patch('controller.agendamento_controller.AgendamentosRepository.existe_conflito')
    def test_criar_agendamento_ambiente_erro_interno(self, mock_conflito, mock_criar,
                                                     client_autenticado):
        """POST /agendamentos com erro no service deve retornar 500"""
        mock_conflito.return_value = False
        mock_criar.return_value = None  # Simula erro
        
        dados = {
            'ambiente_id': 1,
            'data': '2026-02-20',
            'hora_inicio': '09:00',
            'hora_fim': '11:00',
            'finalidade': 'Reunião'
        }
        
        response = client_autenticado.post('/agendamentos',
                                          json=dados)
        
        assert response.status_code == 500
        assert b"erro" in response.data.lower()
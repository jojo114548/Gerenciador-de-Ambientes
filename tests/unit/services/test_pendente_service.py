"""
Testes para pendente_service.py
Cobertura: ~1% do total
Total de testes: 4
"""

import pytest
from unittest.mock import patch, MagicMock


class TestPendenteService:
    """Testes unitários do PendenteService"""
    
    @patch('service.pendente_service.PendenteRepository.inserir')
    def test_criar_pendente_sucesso(self, mock_inserir):
        """Deve criar pendente com sucesso"""
        from service.pendente_service import PendenteService
        
        mock_inserir.return_value = 1
        
        dados = {
            "agendamento_id": 1,
            "user_id": "user-123",
            "status": "pendente"
        }
        
        resultado = PendenteService.criar_pendente(dados)
        
        assert resultado == 1
        mock_inserir.assert_called_once_with(dados)
    
    def test_criar_pendente_sem_user_id(self):
        """Deve lançar erro se user_id não informado"""
        from service.pendente_service import PendenteService
        
        dados = {
            "agendamento_id": 1,
            "status": "pendente"
            # Faltando user_id
        }
        
        with pytest.raises(ValueError, match="Usuário não informado"):
            PendenteService.criar_pendente(dados)
    
    @patch('service.pendente_service.PendenteRepository.listar')
    def test_listar_pendentes(self, mock_listar, mock_pendente):
        """Deve listar pendentes"""
        from service.pendente_service import PendenteService
        
        mock_listar.return_value = [mock_pendente]
        
        resultado = PendenteService.listar()
        
        assert len(resultado) == 1
        assert resultado[0]["status"] == "pendente"
        mock_listar.assert_called_once()
    
    @patch('service.pendente_service.PendenteRepository.atualizar_status')
    @patch('service.pendente_service.HistoricoService.criar_historico')
    @patch('service.pendente_service.AgendamentosRepository.existe_conflito')
    @patch('service.pendente_service.PendenteRepository.buscar_por_id')
    def test_atualizar_status_confirmado(self, mock_buscar, mock_conflito,
                                         mock_historico, mock_atualizar,
                                         mock_pendente):
        """Deve atualizar status e criar histórico"""
        from service.pendente_service import PendenteService
        
        mock_buscar.return_value = mock_pendente
        mock_conflito.return_value = False
        
        resultado = PendenteService.atualizar_status(1, "Confirmado")
        
        mock_atualizar.assert_called_once_with(1, "Confirmado")
        mock_historico.assert_called_once()
        assert resultado["id"] == 1
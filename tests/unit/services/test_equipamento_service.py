"""
Testes para equipamento_service.py
Cobertura: ~2% do total
Total de testes: 5
"""

import pytest
from unittest.mock import patch, MagicMock


class TestEquipamentoService:
    """Testes unitários do EquipamentoService"""
    
    @patch('service.equipamento_service.EquipamentoRepository.listar')
    def test_listar_equipamentos_com_especificacoes(self, mock_listar):
        """Deve listar equipamentos e separar especificações"""
        from service.equipamento_service import EquipamentoService
        
        mock_listar.return_value = [
            {
                "id": 1,
                "name": "Projetor",
                "especificacoes": "Full HD | HDMI | 3000 lumens"
            },
            {
                "id": 2,
                "name": "Notebook",
                "especificacoes": None
            }
        ]
        
        resultado = EquipamentoService.listar()
        
        assert len(resultado) == 2
        assert resultado[0]["especificacoes"] == ["Full HD", "HDMI", "3000 lumens"]
        assert resultado[1]["especificacoes"] == []
    
    @patch('service.equipamento_service.EquipamentoRepository.inserir_especificacoes')
    @patch('service.equipamento_service.EquipamentoRepository.inserir_equipamento')
    def test_inserir_equipamento_com_especificacoes(self, mock_inserir, mock_specs):
        """Deve inserir equipamento e especificações"""
        from service.equipamento_service import EquipamentoService
        
        mock_inserir.return_value = 1
        
        dados = {
            "name": "Projetor Epson",
            "categoria": "audio_video",
            "status": "Disponivel",
            "quantidade_disponivel": 5,
            "especificacoes": ["Full HD", "HDMI"]
        }
        
        equipamento_id = EquipamentoService.inserir_equipamento(dados)
        
        assert equipamento_id == 1
        mock_inserir.assert_called_once()
        mock_specs.assert_called_once_with(1, ["Full HD", "HDMI"])
    
    @patch('service.equipamento_service.EquipamentoRepository.inserir_especificacoes')
    @patch('service.equipamento_service.EquipamentoRepository.inserir_equipamento')
    def test_inserir_equipamento_sem_quantidade(self, mock_inserir, mock_specs):
        """Deve lançar erro se quantidade não informada"""
        from service.equipamento_service import EquipamentoService
        
        dados = {
            "name": "Projetor",
            "categoria": "audio_video",
            "quantidade_disponivel": None  # Inválido
        }
        
        with pytest.raises(ValueError, match="Quantidade disponível é obrigatória"):
            EquipamentoService.inserir_equipamento(dados)
    
    @patch('service.equipamento_service.EquipamentoRepository.atualizar_equipamento')
    def test_atualizar_equipamento_quantidade_zero(self, mock_atualizar):
        """Deve marcar como Ocupado se quantidade for zero"""
        from service.equipamento_service import EquipamentoService
        
        dados = {
            "id": 1,
            "name": "Projetor",
            "categoria": "audio_video",
            "status": "Disponivel",
            "quantidade_disponivel": 0
        }
        
        EquipamentoService.atualizar_equipamento(dados)
        
        # Verifica se foi chamado e status mudou para Ocupado
        mock_atualizar.assert_called_once()
        call_args = mock_atualizar.call_args[0][0]
        assert call_args.status == "Ocupado"
    
    @patch('service.equipamento_service.EquipamentoRepository.deletar_equipamento')
    def test_deletar_equipamento(self, mock_deletar):
        """Deve deletar equipamento"""
        from service.equipamento_service import EquipamentoService
        
        EquipamentoService.deletar_equipamento(1)
        
        mock_deletar.assert_called_once_with(1)
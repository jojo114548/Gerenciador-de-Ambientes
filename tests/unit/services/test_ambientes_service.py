"""
Testes para ambientes_service.py
Cobertura: ~3% do total
Total de testes: 5
"""

import pytest
from unittest.mock import patch, MagicMock


class TestAmbientesService:
    """Testes unitários do AmbientesService"""
    
    @patch('service.ambientes_service.AmbientesRepository.listar')
    def test_listar_ambientes_com_recursos(self, mock_listar):
        """Deve listar ambientes e separar recursos"""
        from service.ambientes_service import AmbientesService
        
        mock_listar.return_value = [
            {
                "id": 1,
                "name": "Sala A",
                "recursos": "TV | Projetor | Quadro"
            },
            {
                "id": 2,
                "name": "Sala B",
                "recursos": None
            }
        ]
        
        resultado = AmbientesService.listar()
        
        assert len(resultado) == 2
        assert resultado[0]["recursos"] == ["TV", "Projetor", "Quadro"]
        assert resultado[1]["recursos"] == []
    
    @patch('service.ambientes_service.AmbientesRepository.inserir_recursos')
    @patch('service.ambientes_service.AmbientesRepository.inserir_ambiente')
    def test_inserir_ambiente_com_recursos(self, mock_inserir, mock_recursos):
        """Deve inserir ambiente e seus recursos"""
        from service.ambientes_service import AmbientesService
        
        mock_inserir.return_value = 1
        
        dados = {
            "name": "Sala Nova",
            "type": "sala",
            "capacidade": 20,
            "status": "Disponivel",
            "descricao": "Sala moderna",
            "localizacao": "1º andar",
            "area": "30m²",
            "image": "/static/imgs/sala.jpg",
            "recursos": ["TV", "Projetor"]
        }
        
        AmbientesService.inserir_ambiente(dados)
        
        mock_inserir.assert_called_once()
        mock_recursos.assert_called_once_with(1, ["TV", "Projetor"])
    
    @patch('service.ambientes_service.AmbientesRepository.inserir_recursos')
    @patch('service.ambientes_service.AmbientesRepository.inserir_ambiente')
    def test_inserir_ambiente_sem_recursos(self, mock_inserir, mock_recursos):
        """Deve inserir ambiente sem recursos"""
        from service.ambientes_service import AmbientesService
        
        mock_inserir.return_value = 1
        
        dados = {
            "name": "Sala Simples",
            "type": "sala",
            "capacidade": 10,
            "status": "Disponivel",
            "recursos": []
        }
        
        AmbientesService.inserir_ambiente(dados)
        
        mock_inserir.assert_called_once()
        mock_recursos.assert_not_called()
    
    @patch('service.ambientes_service.AmbientesRepository.atualizar_recursos')
    @patch('service.ambientes_service.AmbientesRepository.atualizar_ambiente')
    def test_atualizar_ambiente_com_recursos(self, mock_atualizar, mock_recursos):
        """Deve atualizar ambiente e recursos"""
        from service.ambientes_service import AmbientesService
        
        dados = {
            "id": 1,
            "name": "Sala Atualizada",
            "type": "sala",
            "capacidade": 25,
            "status": "Disponivel",
            "recursos": ["TV", "Ar Condicionado"]
        }
        
        AmbientesService.atualizar_ambiente(dados)
        
        mock_atualizar.assert_called_once()
        mock_recursos.assert_called_once_with(1, ["TV", "Ar Condicionado"])
    
    @patch('service.ambientes_service.AmbientesRepository.deletar_ambiente')
    def test_deletar_ambiente(self, mock_deletar):
        """Deve deletar ambiente"""
        from service.ambientes_service import AmbientesService
        
        AmbientesService.deletar_ambiente(1)
        
        mock_deletar.assert_called_once_with(1)
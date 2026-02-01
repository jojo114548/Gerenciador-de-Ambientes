"""
Testes para eventos_service.py
Cobertura: ~4% do total
Total de testes: 8
"""

import pytest
from unittest.mock import patch, MagicMock


class TestEventosService:
    """Testes unitários do EventosService"""
    
    @patch('service.eventos_service.EventosRepository.listar')
    @patch('service.eventos_service.EventosRepository.buscar_equipamentos_do_evento')
    def test_listar_eventos(self, mock_equipamentos, mock_listar):
        """Deve listar eventos com equipamentos"""
        from service.eventos_service import EventosService
        
        mock_listar.return_value = [
            {"id": 1, "titulo": "Evento 1"},
            {"id": 2, "titulo": "Evento 2"}
        ]
        mock_equipamentos.side_effect = [
            [{"id": 1, "name": "Projetor"}],
            []
        ]
        
        resultado = EventosService.listar()
        
        assert len(resultado) == 2
        assert resultado[0]["equipamentos"][0]["name"] == "Projetor"
        assert resultado[1]["equipamentos"] == []
    
    @patch('service.eventos_service.NotificacaoService.criar_notificacao')
    @patch('service.eventos_service.RecursosRepository.adicionar_equipamentos_evento')
    @patch('service.eventos_service.EventosRepository.inserir')
    @patch('service.eventos_service.RecursosRepository.verificar_disponibilidade_equipamento')
    @patch('service.eventos_service.RecursosRepository.buscar_equipamento_por_id')
    @patch('service.eventos_service.RecursosRepository.verificar_disponibilidade_ambiente')
    @patch('service.eventos_service.RecursosRepository.buscar_ambiente_por_id')
    def test_criar_evento_sucesso(self, mock_amb, mock_disp_amb, mock_equip,
                                  mock_disp_equip, mock_inserir, mock_add_equip,
                                  mock_notif):
        """Deve criar evento com validações corretas"""
        from service.eventos_service import EventosService
        
        mock_amb.return_value = {"id": 1, "capacidade": 50}
        mock_disp_amb.return_value = True
        mock_equip.return_value = {"id": 1, "name": "Projetor"}
        mock_disp_equip.return_value = True
        mock_inserir.return_value = 1
        
        dados = {
            "titulo": "Workshop",
            "data_evento": "2026-02-15",
            "hora_evento": "14:00",
            "ambiente_id": 1,
            "capacidade": 30,
            "instrutor": "Prof. João",
            "tipo": "workshop"
        }
        
        equipamentos = [{"equipamento_id": 1, "quantidade": 2}]
        
        evento_id = EventosService.criar(dados, equipamentos)
        
        assert evento_id == 1
        mock_inserir.assert_called_once()
        mock_add_equip.assert_called_once()
    
    @patch('service.eventos_service.RecursosRepository.buscar_ambiente_por_id')
    def test_criar_evento_sem_campos_obrigatorios(self, mock_amb):
        """Deve lançar erro se faltam campos obrigatórios"""
        from service.eventos_service import EventosService
        
        dados = {
            "titulo": "Evento",
            # Faltando campos obrigatórios
        }
        
        with pytest.raises(ValueError, match="obrigatório"):
            EventosService.criar(dados)
    
    @patch('service.eventos_service.RecursosRepository.buscar_ambiente_por_id')
    def test_criar_evento_ambiente_nao_encontrado(self, mock_amb):
        """Deve lançar erro se ambiente não existe"""
        from service.eventos_service import EventosService
        
        mock_amb.return_value = None
        
        dados = {
            "titulo": "Workshop",
            "data_evento": "2026-02-15",
            "hora_evento": "14:00",
            "ambiente_id": 999,
            "capacidade": 30,
            "instrutor": "Prof. João",
            "tipo": "workshop"
        }
        
        with pytest.raises(ValueError, match="Ambiente não encontrado"):
            EventosService.criar(dados)
    
    @patch('service.eventos_service.RecursosRepository.verificar_disponibilidade_ambiente')
    @patch('service.eventos_service.RecursosRepository.buscar_ambiente_por_id')
    def test_criar_evento_ambiente_indisponivel(self, mock_amb, mock_disp):
        """Deve lançar erro se ambiente está ocupado"""
        from service.eventos_service import EventosService
        
        mock_amb.return_value = {"id": 1, "capacidade": 50}
        mock_disp.return_value = False
        
        dados = {
            "titulo": "Workshop",
            "data_evento": "2026-02-15",
            "hora_evento": "14:00",
            "ambiente_id": 1,
            "capacidade": 30,
            "instrutor": "Prof. João",
            "tipo": "workshop"
        }
        
        with pytest.raises(ValueError, match="já está reservado"):
            EventosService.criar(dados)
    
    @patch('service.eventos_service.EventosRepository.deletar')
    @patch('service.eventos_service.EventosRepository.buscar_por_id')
    def test_remover_evento_sucesso(self, mock_buscar, mock_deletar):
        """Deve remover evento existente"""
        from service.eventos_service import EventosService
        
        mock_buscar.return_value = {"id": 1, "titulo": "Evento"}
        
        EventosService.remover(1)
        
        mock_deletar.assert_called_once_with(1)
    
    @patch('service.eventos_service.EventosRepository.buscar_por_id')
    def test_remover_evento_nao_encontrado(self, mock_buscar):
        """Deve lançar erro se evento não existe"""
        from service.eventos_service import EventosService
        
        mock_buscar.return_value = None
        
        with pytest.raises(ValueError, match="não encontrado"):
            EventosService.remover(999)
    
    @patch('service.eventos_service.NotificacaoService.criar_notificacao')
    @patch('service.eventos_service.EventosRepository.incrementar_participantes')
    @patch('service.eventos_service.EventosRepository.registrar_inscricao')
    @patch('service.eventos_service.EventosRepository.usuario_ja_inscrito')
    @patch('service.eventos_service.EventosRepository.buscar_por_id')
    def test_inscrever_evento_sucesso(self, mock_buscar, mock_inscrito,
                                      mock_registrar, mock_incrementar, mock_notif):
        """Deve inscrever usuário em evento"""
        from service.eventos_service import EventosService
        
        mock_buscar.return_value = {
            "id": 1,
            "titulo": "Workshop",
            "participantes": 10,
            "capacidade": 30
        }
        mock_inscrito.return_value = False
        
        EventosService.inscrever(1, "user-123")
        
        mock_registrar.assert_called_once_with(1, "user-123")
        mock_incrementar.assert_called_once_with(1)
        mock_notif.assert_called_once()
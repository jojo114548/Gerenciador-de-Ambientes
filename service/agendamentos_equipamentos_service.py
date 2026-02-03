from repository.agendamentos_equipamentos_repository import AgendamentoEquipamentoRepository
from service.notificacao_service import NotificacaoService

class AgendamentoEquipamentoService:

    @staticmethod
    def criar_agendamento(dados: dict):
       """
       Cria agendamento Equipamentos
        
       """
     
       return AgendamentoEquipamentoRepository.inserir(dados)

    
from repository.agendamentos_repository import AgendamentosRepository
from service.notificacao_service import NotificacaoService

class AgendamentosService:


    @staticmethod
    def criar_agendamento(dados):

        return AgendamentosRepository.inserir(dados)
    
        


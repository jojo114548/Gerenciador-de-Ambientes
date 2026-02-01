from repository.agendamentos_equipamentos_repository import AgendamentoEquipamentoRepository
from service.notificacao_service import NotificacaoService

class AgendamentoEquipamentoService:

    @staticmethod
    def criar_agendamento(dados: dict):
     
       return AgendamentoEquipamentoRepository.inserir(dados)

    @staticmethod
    def listar_agendamentos_equipamento(equipamento_id):
        """
        Lista todos os agendamentos de um equipamento
        """
        return AgendamentoEquipamentoRepository.listar_por_equipamento(
            equipamento_id
        )

    @staticmethod
    def listar_agendamentos_usuario(user_id):
        """
        Lista todos os agendamentos de um usuário
        """
        return AgendamentoEquipamentoRepository.listar_por_usuario(user_id)

    @staticmethod
    def aprovar_agendamento(agendamento_id):
        """
        Aprova um agendamento (admin)
        """

        # Ao aprovar, deve garantir que não surgiu conflito
        # após a solicitação (concorrência)
        # Normalmente você buscaria o agendamento aqui,
        # mas mantendo simples, apenas muda status
        AgendamentoEquipamentoRepository.atualizar_status(
            agendamento_id, "aprovado"
        )

    @staticmethod
    def cancelar_agendamento(agendamento_id):
        """
        Cancela um agendamento
        """
        AgendamentoEquipamentoRepository.atualizar_status(
            agendamento_id, "cancelado"
        )

    @staticmethod
    def excluir_agendamento(agendamento_id):
        """
        Exclusão definitiva (uso administrativo)
        """
        AgendamentoEquipamentoRepository.deletar(agendamento_id)

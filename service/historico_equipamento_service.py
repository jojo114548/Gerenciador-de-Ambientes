from repository.historico_equipamento_repository import HistoricoEquipamentoRepository


class HistoricoEquipamentoService:

    @staticmethod
    def criar_historico(dados: dict):

        obrigatorios = [
            "agendamento_id",
            "equipamento_id",
            "user_id",
            "equipamento_nome",
            "data_equip",
            "hora_inicio",
            "hora_fim",
            "finalidade",
            "status"
        ]

        for campo in obrigatorios:
            if campo not in dados or dados[campo] is None:
                raise ValueError(f"Campo obrigatório ausente: {campo}")

        return HistoricoEquipamentoRepository.inserir(dados)

    @staticmethod
    def cancelar_historico(historico_equipamentos_id, user_id):
        HistoricoEquipamentoRepository.cancelar(historico_equipamentos_id, user_id)
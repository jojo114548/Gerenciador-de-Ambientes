from repository.historico_repository import HistoricoRepository 



class HistoricoService:

    @staticmethod
    def criar_historico(dados):
        obrigatorios = [
            "user_id", "type", "name",
            "historico_date", "start_time",
            "end_time", "purpose", "status"
        ]

        for campo in obrigatorios:
            if campo not in dados or dados[campo] is None:
                raise ValueError(f"Campo obrigatório ausente: {campo}")

        HistoricoRepository.inserir(dados)
    @staticmethod
    def cancelar_historico(historico_id, user_id):
        HistoricoRepository.cancelar(historico_id, user_id)



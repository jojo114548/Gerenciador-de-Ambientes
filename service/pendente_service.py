from repository.pendente_repository import PendenteRepository
from service.historico_service import HistoricoService
from repository.agendamentos_repository import AgendamentosRepository

class PendenteService:

 
    @staticmethod
    def criar_pendente(dados):
        if not dados:
            raise Exception("Dados do pendente não informados")

        if not dados.get("user_id"):
            raise ValueError("Usuário não informado para criação de pendente")
        
      

        try:
            return PendenteRepository.inserir(dados)
        except Exception as e:
            if "uq_pendente_agendamento" in str(e):
                return None
            raise

    @staticmethod
    def listar():
        return PendenteRepository.listar()

    @staticmethod
    def atualizar_status(pendente_id, status):

        pendente = PendenteRepository.buscar_por_id(pendente_id)

        if not pendente:
            raise Exception("Pendente não encontrado")

        conflito = AgendamentosRepository.existe_conflito(
            ambiente_id=pendente["ambiente_id"],
            data=pendente["data"],
            hora_inicio=pendente["hora_inicio"],
            hora_fim=pendente["hora_fim"],
            agendamento_id=pendente["agendamento_id"]
        )

        if conflito:
            raise ValueError(
                "Conflito de horário: o ambiente já está reservado nesse período."
            )

        # Atualizar status primeiro
        PendenteRepository.atualizar_status(pendente_id, status)

        # ✅ HISTÓRICO DE AMBIENTE
        HistoricoService.criar_historico({
            "agendamento_id": pendente["agendamento_id"],
            "user_id": pendente["user_id"],
            "type": "Ambientes",
            "name": pendente["ambiente_nome"],
            "historico_date": pendente["data"],
            "start_time": pendente["hora_inicio"],
            "end_time": pendente["hora_fim"],
            "purpose": pendente["finalidade"],
            "status": status
        })

        # Retornar os dados atualizados
        return {
            **pendente,
            "status": status
        }
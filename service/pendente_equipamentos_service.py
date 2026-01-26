from repository.pendente_equipamento_repository import PendenteEquipamentoRepository
from service.historico_equipamento_service import HistoricoEquipamentoService
from service.notificacao_service import NotificacaoService


class PendenteServiceEquip:

    @staticmethod
    def criar_pendente(dados):
        if not dados:
            raise Exception("Dados do pendente não informados")

        if not dados.get("user_id"):
            raise ValueError("Usuário não informado para criação de pendente")

        try:
            return PendenteEquipamentoRepository.inserir(dados)
        except Exception as e:
            if "uq_pendente_agendamento" in str(e):
                return None
            raise

    @staticmethod
    def listar():
        return PendenteEquipamentoRepository.listar()

    @staticmethod
    def atualizar_status(pendente_id, status):
        if status not in ["Confirmado", "Rejeitado"]:
            raise ValueError("Status inválido")

        # 1️⃣ Busca antes
        pendente = PendenteEquipamentoRepository.buscar_por_id(pendente_id)
        if not pendente:
            raise Exception("Pendente não encontrado")

        # 2️⃣ Valida campos
        campos = [
            "agendamento_id",
            "equipamento_id",
            "equipamento_nome",
            "data_equip",
            "hora_inicio",
            "hora_fim",
            "finalidade"
        ]

        for campo in campos:
            if pendente.get(campo) is None:
                raise Exception(
                    f"Campo {campo} está NULL — erro no SELECT do repository"
                )

        # 3️⃣ Atualiza status
        PendenteEquipamentoRepository.atualizar_status(
            pendente_id,
            status
        )

        # 4️⃣ Histórico
        HistoricoEquipamentoService.criar_historico({
            "agendamento_id": pendente["agendamento_id"],
            "equipamento_id": pendente["equipamento_id"],
            "user_id": pendente["user_id"],
            "equipamento_nome": pendente["equipamento_nome"],
            "data_equip": pendente["data_equip"],
            "hora_inicio": pendente["hora_inicio"],
            "hora_fim": pendente["hora_fim"],
            "finalidade": pendente["finalidade"],
            "status": status
        })

        # 5️⃣ Notificação
        NotificacaoService.criar_notificacao(
            user_id=pendente["user_id"],
            titulo="Status de Agendamento",
            mensagem=f"Seu agendamento foi {status}.",
            tipo="aviso"
        )

        return pendente
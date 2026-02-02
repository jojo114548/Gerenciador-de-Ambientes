from repository.historico_equipamento_repository import (
    HistoricoEquipamentoRepository
)


class HistoricoEquipamentoService:

  
 
    @staticmethod
    def criar_historico(dados):
        """
        ✅ CORRIGIDO: Validação de campos obrigatórios
        """
        obrigatorios = [
            "agendamento_id",      # ✅ ADICIONADO
            "equipamento_id",      # ✅ ADICIONADO
            "user_id",
            "equipamento_nome",
            "data_equip",          # ✅ CORRIGIDO: era "date_equip"
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
    def cancelar_historico(historicoEquip_id, user_id):

        historico = HistoricoEquipamentoRepository.buscar_por_id(historicoEquip_id)
        
        if not user_id:
            raise({'error': 'Usuário não autenticado'})

        if not historico:
            raise ValueError("Histórico não encontrado")
        

        if historico["user_id"] != user_id:
            raise PermissionError("Sem permissão")

        HistoricoEquipamentoRepository.atualizar_status_por_id(
            historicoEquip_id,
            "Cancelado"
        )

    @staticmethod
    def atualizar_concluidos():
        return HistoricoEquipamentoRepository.marcar_concluidos()
    


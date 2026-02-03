from repository.historico_equipamento_repository import (
    HistoricoEquipamentoRepository
)


class HistoricoEquipamentoService:

  
 
    @staticmethod
    def criar_historico(dados):
        """
        Cria um novo registro de histórico de equipamento.

        Responsabilidades:
        - Validar a presença de todos os campos obrigatórios
        - Garantir integridade mínima dos dados
        - Persistir o histórico no banco de dados

        """
        
          # Lista de campos obrigatórios para criação do histórico
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
        
        # Validação de todos os campos obrigatórios
        for campo in obrigatorios:
            if campo not in dados or dados[campo] is None:
                raise ValueError(f"Campo obrigatório ausente: {campo}")
            
        # Insere o histórico no banco e retorna o resultado
        return HistoricoEquipamentoRepository.inserir(dados)


    @staticmethod
    def cancelar_historico(historicoEquip_id, user_id):
        """
        Cancela um histórico de equipamento.

        Fluxo:
        - Busca o histórico pelo ID
        - Valida se o usuário está autenticado
        - Verifica se o histórico existe
        - Confere permissão (usuário dono do histórico)
        - Atualiza o status para 'Cancelado'
        """
        # Busca o histórico no banco de dados
        historico = HistoricoEquipamentoRepository.buscar_por_id(historicoEquip_id)
        
        # Valida se o usuário está autenticado
        if not user_id:
            raise({'error': 'Usuário não autenticado'})
        
        # Valida se o histórico existe
        if not historico:
            raise ValueError("Histórico não encontrado")
        
        # Verifica se o usuário tem permissão para cancelar
        if historico["user_id"] != user_id :
            raise PermissionError("Sem permissão")
        
        # Atualiza o status do histórico para Cancelado
        HistoricoEquipamentoRepository.atualizar_status_por_id(
            historicoEquip_id,
            "Cancelado"
        )

    @staticmethod
    def atualizar_concluidos():
        """
        Atualiza automaticamente os históricos concluídos .

        """
        return HistoricoEquipamentoRepository.marcar_concluidos()
    


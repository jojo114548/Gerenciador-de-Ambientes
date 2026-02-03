from repository.historico_repository import HistoricoRepository



class HistoricoService:

    @staticmethod
    def criar_historico(dados):
        """
        Cria um novo registro de histórico.

        Responsabilidades:
        - Valida a existência de todos os campos obrigatórios
        - Garante integridade mínima dos dados
        - Persiste o histórico no banco de dados
        """

        # Lista de campos obrigatórios para criação do histórico
        obrigatorios = [
            "user_id", "type", "name",
            "historico_date", "start_time",
            "end_time", "purpose", "status"
        ]
         # Validação dos campos obrigatórios
        for campo in obrigatorios:
            if campo not in dados or dados[campo] is None:
                raise ValueError(f"Campo obrigatório ausente: {campo}")
        # Insere o histórico no banco de dados
        HistoricoRepository.inserir(dados)



    @staticmethod
    def cancelar_historico(historico_id, user_id):
        """
        Cancela um histórico existente.

        Fluxo:
        - Busca o histórico pelo ID
        - Valida se o histórico existe
        - Verifica se o usuário é o dono do histórico
        - Atualiza o status para 'Cancelado'
        """
        # Busca o histórico no banco pelo ID
        historico = HistoricoRepository.buscar_por_id(historico_id)
        
        # Valida existência do histórico
        if not historico:
            raise ValueError("Histórico não encontrado")
        
         # Verifica se o usuário tem permissão para cancelar
        if historico["user_id"] != user_id:
            raise PermissionError("Sem permissão para cancelar")
        
         # Atualiza o status do histórico para Cancelado
        HistoricoRepository.atualizar_status_por_id(
            historico_id,
            "Cancelado"
        )

    @staticmethod
    def atualizar_concluidos():
       """
        Atualiza automaticamente históricos concluídos apos data e hora .

       """
       return HistoricoRepository.marcar_concluidos()



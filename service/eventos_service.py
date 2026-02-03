

from repository.eventos_repository import EventosRepository
from repository.recursosEventos_repository import RecursosRepository
from service.notificacao_service import NotificacaoService


class EventosService:
    

    @staticmethod
    def listar():
        """
        Lista todos os eventos cadastrados no sistema.
        
        Funcionalidade:
        - Recupera todos os eventos do banco de dados
        - Para cada evento, busca os equipamentos vinculados
        - Anexa a lista de equipamentos ao objeto do evento
        
        Returns:
            list: Lista de dicionários contendo os eventos com seus equipamentos
        """
        # Busca todos os eventos cadastrados no banco de dados
        eventos = EventosRepository.listar()
        
        # Busca os equipamentos associados a cada evento
        for evento in eventos:
            # Busca equipamentos 
            equipamentos = EventosRepository.buscar_equipamentos_do_evento(evento["id"])
            # Adiciona a lista de equipamentos ao dicionário do evento
            evento["equipamentos"] = equipamentos

        return eventos

    @staticmethod
    def criar(dados, equipamentos=None):
        """
        Cria um novo evento no sistema com todas as validações necessárias.
        
        Funcionalidade:
        - Valida a presença de todos os campos obrigatórios
        - Valida os valores de capacidade e participantes
        - Verifica a existência e disponibilidade do ambiente solicitado
        - Verifica a disponibilidade dos equipamentos (se fornecidos)
        - Garante que a capacidade do evento não exceda a do ambiente
        - Insere o evento no banco de dados
        - Vincula os equipamentos ao evento criado
        
        Args:
            dados (dict): Dicionário com os dados do evento (título, data, hora, etc.)
            equipamentos (list, optional): Lista de equipamentos a serem vinculados ao evento
            
        Returns:
            int: ID do evento criado
            
        Raises:
            ValueError: Se alguma validação falhar (campo ausente, capacidade inválida, 
                       ambiente indisponível, equipamento indisponível, etc.)
        """

        # Lista de campos obrigatórios para criação do evento
        campos_obrigatorios = [
            "titulo", "data_evento", "hora_evento",
            "ambiente_id", "capacidade", "instrutor", "tipo"
        ]
        
        # Validação de campos obrigatórios - verifica se todos estão presentes
        for campo in campos_obrigatorios:
            if not dados.get(campo):
                raise ValueError(f"Campo obrigatório ausente: {campo}")
        
        # Conversão dos valores de capacidade e participantes para inteiro
        capacidade = int(dados.get("capacidade"))
        participantes = int(dados.get("participantes", 0))
        
        # Validação: capacidade deve ser maior que zero
        if capacidade <= 0:
            raise ValueError("Capacidade deve ser maior que zero")
        
        # Validação: número de participantes não pode exceder a capacidade total
        if participantes > capacidade:
            raise ValueError("Participantes não podem exceder a capacidade")
        
        # Busca o ambiente associado ao evento pelo ID fornecido
        ambiente = RecursosRepository.buscar_ambiente_por_id(dados["ambiente_id"])
        if not ambiente:
            raise ValueError("Ambiente não encontrado")
        
        # Verifica se o ambiente está disponível (não reservado) na data e hora informadas
        if not RecursosRepository.verificar_disponibilidade_ambiente(
            dados["ambiente_id"],
            dados["data_evento"],
            dados["hora_evento"]
        ):
            raise ValueError("Ambiente já está reservado para este horário")
        
        # Validação: capacidade do evento não pode exceder a capacidade física do ambiente
        if capacidade > ambiente["capacidade"]:
            raise ValueError(
                f"Capacidade do evento ({capacidade}) excede a capacidade do ambiente ({ambiente['capacidade']})"
            )
        
        # Caso existam equipamentos a serem vinculados ao evento
        if equipamentos:
            for equip in equipamentos:
                # Verifica se o equipamento existe no banco de dados através do ID
                equipamento = RecursosRepository.buscar_equipamento_por_id(equip["equipamento_id"])

                if not equipamento:
                    raise ValueError(f"Equipamento ID {equip['equipamento_id']} não encontrado")
                
                # Verifica se o equipamento está disponível na quantidade solicitada para a data/hora
                if not RecursosRepository.verificar_disponibilidade_equipamento(
                    equip["equipamento_id"],
                    equip["quantidade"],
                    dados["data_evento"],
                    dados["hora_evento"]
                ):
                    raise ValueError(
                        f"Equipamento '{equipamento['name']}' não disponível na quantidade solicitada"
                    )
        
        # Insere o evento no banco de dados e retorna o ID gerado
        evento_id = EventosRepository.inserir(dados)

        # Se houver equipamentos, vincula-os ao evento recém-criado
        if equipamentos:
            RecursosRepository.adicionar_equipamentos_evento(evento_id, equipamentos)

        return evento_id

    @staticmethod
    def remover(id):
        """
        Remove um evento do sistema pelo seu ID.
        
        Funcionalidade:
        - Verifica se o evento existe no banco de dados
        - Remove o evento se ele existir
        
        Args:
            id (int): ID do evento a ser removido
            
        Raises:
            ValueError: Se o evento não for encontrado
        """
        # Busca o evento no banco de dados pelo ID fornecido
        evento = EventosRepository.buscar_por_id(id)

        # Se o evento não existir, lança erro
        if not evento:
            raise ValueError("Agendamento não encontrado")

        # Remove o evento do banco de dados
        EventosRepository.deletar(id)

    @staticmethod
    def inscrever(evento_id, user_id):
        """
        Realiza a inscrição de um usuário em um evento específico.
        
        Funcionalidade:
        - Verifica se o evento existe
        - Verifica se há vagas disponíveis (capacidade não atingida)
        - Verifica se o usuário já está inscrito no evento
        - Registra a inscrição do usuário
        - Incrementa o contador de participantes do evento
        
        Args:
            evento_id (int): ID do evento no qual o usuário deseja se inscrever
            user_id (int): ID do usuário que deseja se inscrever
            
        Raises:
            ValueError: Se o evento não existir, estiver lotado ou usuário já estiver inscrito
        """
        # Busca o evento no banco de dados pelo ID fornecido
        evento = EventosRepository.buscar_por_id(evento_id)
       
        # Se o evento não existir, lança erro
        if not evento:
            raise ValueError("Evento não encontrado")
        
        # Verifica se o evento já atingiu a capacidade máxima de participantes
        if evento["participantes"] >= evento["capacidade"]:
            raise ValueError("Evento lotado")
        
        # Verifica se o usuário já está inscrito no evento para evitar duplicação
        if EventosRepository.usuario_ja_inscrito(evento_id, user_id):
            raise ValueError("Usuário já inscrito")
        
        # Registra a inscrição do usuário no evento
        EventosRepository.registrar_inscricao(evento_id, user_id)
        # Incrementa o contador de participantes do evento
        EventosRepository.incrementar_participantes(evento_id)


    @staticmethod
    def buscar_detalhes(evento_id):
        """
        Busca os detalhes completos de um evento específico, incluindo seus equipamentos.
        
        """
         # Busca o evento pelo ID no banco de dados
        evento = EventosRepository.buscar_por_id(evento_id)

         # Se o evento existir
        if evento:
             # Lista todos os equipamentos vinculados ao evento
            evento["equipamentos"] = RecursosRepository.listar_equipamentos_evento(evento_id)
        return evento

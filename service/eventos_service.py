from repository.eventos_repository import EventosRepository
from repository.recursosEventos_repository import RecursosRepository
from service.notificacao_service import NotificacaoService


class EventosService:

    @staticmethod
    def listar():
        eventos = EventosRepository.listar()

        for evento in eventos:
            equipamentos = EventosRepository.buscar_equipamentos_do_evento(evento["id"])
            evento["equipamentos"] = equipamentos

        return eventos

    @staticmethod
    def criar(dados, equipamentos=None):
        campos_obrigatorios = [
            "titulo", "data_evento", "hora_evento",
            "ambiente_id", "capacidade", "instrutor", "tipo"
        ]

        for campo in campos_obrigatorios:
            if not dados.get(campo):
                raise ValueError(f"Campo obrigatório ausente: {campo}")

        capacidade = int(dados.get("capacidade"))
        participantes = int(dados.get("participantes", 0))

        if capacidade <= 0:
            raise ValueError("Capacidade deve ser maior que zero")

        if participantes > capacidade:
            raise ValueError("Participantes não podem exceder a capacidade")

        ambiente = RecursosRepository.buscar_ambiente_por_id(dados["ambiente_id"])
        if not ambiente:
            raise ValueError("Ambiente não encontrado")

        if not RecursosRepository.verificar_disponibilidade_ambiente(
            dados["ambiente_id"],
            dados["data_evento"],
            dados["hora_evento"]
        ):
            raise ValueError("Ambiente já está reservado para este horário")

        if capacidade > ambiente["capacidade"]:
            raise ValueError(
                f"Capacidade do evento ({capacidade}) excede a capacidade do ambiente ({ambiente['capacidade']})"
            )

        if equipamentos:
            for equip in equipamentos:
                equipamento = RecursosRepository.buscar_equipamento_por_id(equip["equipamento_id"])
                if not equipamento:
                    raise ValueError(f"Equipamento ID {equip['equipamento_id']} não encontrado")

                if not RecursosRepository.verificar_disponibilidade_equipamento(
                    equip["equipamento_id"],
                    equip["quantidade"],
                    dados["data_evento"],
                    dados["hora_evento"]
                ):
                    raise ValueError(
                        f"Equipamento '{equipamento['name']}' não disponível na quantidade solicitada"
                    )

        evento_id = EventosRepository.inserir(dados)

        if equipamentos:
            RecursosRepository.adicionar_equipamentos_evento(evento_id, equipamentos)

        return evento_id

    @staticmethod
    def remover(id):
        evento = EventosRepository.buscar_por_id(id)
        if not evento:
            raise ValueError("Agendamento não encontrado")

        EventosRepository.deletar(id)

    @staticmethod
    def inscrever(evento_id, user_id):
        evento = EventosRepository.buscar_por_id(evento_id)

        if not evento:
            raise ValueError("Evento não encontrado")

        if evento["participantes"] >= evento["capacidade"]:
            raise ValueError("Evento lotado")

        if EventosRepository.usuario_ja_inscrito(evento_id, user_id):
            raise ValueError("Usuário já inscrito")

        EventosRepository.registrar_inscricao(evento_id, user_id)
        EventosRepository.incrementar_participantes(evento_id)

        try:
            NotificacaoService.criar_notificacao(
                user_id=user_id,
                titulo="Inscrição confirmada",
                mensagem=f"Você foi inscrito no evento '{evento['titulo']}'.",
                tipo="sucesso"
            )
        except Exception as e:
            print("Falha ao criar notificação:", e)

    @staticmethod
    def atualizar(id, dados, equipamentos=None):
        evento_antigo = EventosRepository.buscar_por_id(id)
        if not evento_antigo:
            raise ValueError("Evento não encontrado")

        if dados.get("ambiente_id") and dados["ambiente_id"] != evento_antigo["ambiente_id"]:
            ambiente = RecursosRepository.buscar_ambiente_por_id(dados["ambiente_id"])
            if not ambiente:
                raise ValueError("Ambiente não encontrado")

            if not RecursosRepository.verificar_disponibilidade_ambiente(
                dados["ambiente_id"],
                dados.get("data_evento", evento_antigo["data_evento"]),
                dados.get("hora_evento", evento_antigo["hora_evento"])
            ):
                raise ValueError("Ambiente já está reservado para este horário")

        if equipamentos is not None:
            RecursosRepository.remover_equipamentos_evento(id)

            if equipamentos:
                for equip in equipamentos:
                    if not RecursosRepository.verificar_disponibilidade_equipamento(
                        equip["equipamento_id"],
                        equip["quantidade"],
                        dados.get("data_evento", evento_antigo["data_evento"]),
                        dados.get("hora_evento", evento_antigo["hora_evento"])
                    ):
                        equipamento = RecursosRepository.buscar_equipamento_por_id(equip["equipamento_id"])
                        raise ValueError(f"Equipamento '{equipamento['name']}' não disponível")

                RecursosRepository.adicionar_equipamentos_evento(id, equipamentos)

        atualizado = EventosRepository.atualizar(id, dados)

        if atualizado:
            NotificacaoService.criar_notificacao(
                user_id="admin",
                titulo="Evento atualizado",
                mensagem=f"O evento '{evento_antigo['titulo']}' foi alterado.",
                tipo="info"
            )

        return atualizado

    @staticmethod
    def buscar_detalhes(evento_id):
        evento = EventosRepository.buscar_por_id(evento_id)
        if evento:
            evento["equipamentos"] = RecursosRepository.listar_equipamentos_evento(evento_id)
        return evento

from repository.notificacao_repository import NotificacaoRepository


class NotificacaoService:

    TIPOS_VALIDOS = {"info", "aviso", "sucesso"}

    @staticmethod
    def criar_notificacao(user_id, titulo, mensagem, tipo="info"):
        if not titulo or not mensagem:
            raise ValueError("Título e mensagem são obrigatórios")

        # Blindagem contra ENUM inválido
        if tipo not in NotificacaoService.TIPOS_VALIDOS:
            tipo = "info"

        NotificacaoRepository.criar(
            user_id,
            titulo,
            mensagem,
            tipo
        )

    @staticmethod
    def listar_nao_lidas(user_id):
        return NotificacaoRepository.listar_nao_lidas(user_id)

    @staticmethod
    def marcar_lida(notificacao_id):
        return NotificacaoRepository.marcar_como_lida(notificacao_id)

    @staticmethod
    def total_nao_lidas(user_id):
        return NotificacaoRepository.contar_nao_lidas(user_id)

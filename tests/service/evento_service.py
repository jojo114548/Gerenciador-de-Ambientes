class EventoService:

    @staticmethod
    def marcar_inscricao(eventos, usuario_id, repo):
        for evento in eventos:
            evento["inscrito"] = repo.usuario_ja_inscrito(
                evento["id"], usuario_id
            )
        return eventos

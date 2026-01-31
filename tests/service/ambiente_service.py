class AmbienteService:

    @staticmethod
    def listar_ambientes(repo):
        ambientes = repo.listar()

        if ambientes is None:
            raise ValueError("Erro ao buscar ambientes")

        return ambientes

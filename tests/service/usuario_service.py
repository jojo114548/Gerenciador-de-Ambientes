class UsuarioService:

    @staticmethod
    def validar_usuario(usuario):
        if not usuario.get("email"):
            raise ValueError("Email obrigatório")

        if not usuario.get("senha"):
            raise ValueError("Senha obrigatória")

        return True

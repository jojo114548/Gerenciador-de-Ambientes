import bcrypt
from repository.usuario_repository import UsuarioRepository
from service.notificacao_service import NotificacaoService
from model.usuarios import Usuario
from datetime import datetime


class UsuarioService:

    @staticmethod
    def listar():
        return UsuarioRepository.listar()

    @staticmethod
    def cadastrar(dados):
        campos_obrigatorios = [
            "name", "email", "senha", "role", "status",
            "cpf", "data_nascimento"
        ]

        for campo in campos_obrigatorios:
            if campo not in dados or not dados[campo]:
                raise ValueError(f"Campo obrigatório ausente: {campo}")
        
        email_existente = UsuarioRepository.buscar_por_email(dados["email"])
        if email_existente:
            raise ValueError("Este email já está cadastrado no sistema")
        
        if dados.get("data_nascimento"):
            dados["data_nascimento"] = datetime.strptime(
                dados["data_nascimento"], "%Y-%m-%d"
            ).date()
        
        # Hash da senha
        dados["senha"] = bcrypt.hashpw(
            dados["senha"].encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        # Garante campos opcionais
        dados.setdefault("rg", None)
        dados.setdefault("telefone", None)
        dados.setdefault("endereco", None)
        dados.setdefault("departamento", None)
        dados.setdefault("funcao", None)
        dados.setdefault("image", None)

        # Cria usuário
        users = Usuario(**dados)
        UsuarioRepository.adicionar(users)

        
        # ✅ RETORNE UM DICIONÁRIO, NÃO O OBJETO
        return {
            "id": users.id,
            "name": users.name,
            "email": users.email
        }

    @staticmethod
    def atualizar(id, dados):
        if not id:
            raise ValueError("ID do usuário é obrigatório")

        UsuarioRepository.atualizar(id, dados)

       

    @staticmethod
    def deletar(usuario_id):
        if not usuario_id:
            raise ValueError("ID do usuário é obrigatório")

        UsuarioRepository.deletar(usuario_id)

        
    @staticmethod
    def autenticar(email, senha):
        usuario = UsuarioRepository.buscar_por_email(email)

        if not usuario:
            return None

        if bcrypt.checkpw(
            senha.encode("utf-8"),
            usuario["senha"].encode("utf-8")
        ):
            return usuario

        return None

    @staticmethod
    def alterar_senha(usuario_id, senha):
        if not usuario_id or not senha:
            raise ValueError("Usuário e senha são obrigatórios")

        senha_hash = bcrypt.hashpw(
            senha.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        UsuarioRepository.atualizar_senha(usuario_id, senha_hash)

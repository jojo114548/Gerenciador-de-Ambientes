import bcrypt
from repository.usuario_repository import UsuarioRepository
from service.notificacao_service import NotificacaoService
from model.usuarios import Usuario
from datetime import datetime
from model.usuarios import Usuario
import uuid,os,bcrypt

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

        return {
            "id": users.id,
            "name": users.name,
            "email": users.email
        }

    @staticmethod
    def atualizar(usuario_id, dados):
        if not UsuarioRepository._existe(usuario_id):
            raise ValueError("Usuário não encontrado")

        # Remove image se não foi enviada
        if "image" in dados and dados["image"] is None:
            dados.pop("image")

        UsuarioRepository.atualizar(usuario_id, dados)

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

        senha_hash = usuario.get("senha")

        # Proteção contra senha inválida no banco
        if not senha_hash or not isinstance(senha_hash, str) or not senha_hash.startswith("$2"):
            print(f"[ERRO] Hash inválido para usuário {email}")
            return None

        try:
            if bcrypt.checkpw(
                senha.encode("utf-8"),
                senha_hash.encode("utf-8")
            ):
                return usuario
        except ValueError:
            # Segurança extra caso algo passe
            print(f"[ERRO] bcrypt inválido para usuário {email}")
            return None

        return None


    # ✅ Método para o próprio usuário alterar sua senha
    @staticmethod
    def alterar_senha(usuario_id, senha_atual, senha_nova):
        if not usuario_id or not senha_atual or not senha_nova:
            raise ValueError("Todos os campos são obrigatórios")

        # Busca o usuário
        usuario = UsuarioRepository.buscar_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado")

        # Verifica se a senha atual está correta
        if not bcrypt.checkpw(
            senha_atual.encode("utf-8"),
            usuario["senha"].encode("utf-8")
        ):
            raise ValueError("Senha atual incorreta")

        # Gera hash da nova senha
        senha_hash = bcrypt.hashpw(
            senha_nova.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        # Atualiza a senha
        UsuarioRepository.atualizar_senha(usuario_id, senha_hash)

    # ✅ Método para admin resetar senha sem precisar da senha atual
    @staticmethod
    def resetar_senha(usuario_id, senha_nova):
        if not usuario_id or not senha_nova:
            raise ValueError("Usuário e senha são obrigatórios")

        # Verifica se usuário existe
        if not UsuarioRepository._existe(usuario_id):
            raise ValueError("Usuário não encontrado")

        # Gera hash da nova senha
        senha_hash = bcrypt.hashpw(
            senha_nova.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        # Atualiza a senha
        UsuarioRepository.atualizar_senha(usuario_id, senha_hash)

    @staticmethod
    def resetar_senha_padrao(usuario_id):
        if not usuario_id:
            raise ValueError("Usuário é obrigatório")

        usuario = UsuarioRepository.buscar_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado")

        cpf = usuario.get("cpf")

        if not cpf or len(cpf) < 4:
            raise ValueError("CPF inválido para gerar senha padrão")

        # Últimos 4 dígitos do CPF
        ultimos_4 = cpf[-4:]

        senha_padrao = f"User#{ultimos_4}"

        senha_hash = bcrypt.hashpw(
            senha_padrao.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        UsuarioRepository.atualizar_senha(usuario_id, senha_hash)

        # (Opcional) Notificação
        # NotificacaoService.enviar_reset_senha(usuario_id)

        return True
    
    @staticmethod
    def garantir_admin_padrao():
        email_admin = "admin@nexus.com"

        admin_existente = UsuarioRepository.buscar_por_email(email_admin)
        if admin_existente:
            return

        senha_hash = bcrypt.hashpw(
            "Admin@123".encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        admin = Usuario(
            id=str(uuid.uuid4()),
            name="Administrador",
            email=email_admin,
            cpf="00000000000",
            rg=None,
            data_nascimento=datetime.strptime("1990-01-01", "%Y-%m-%d").date(),
            telefone=None,
            endereco=None,
            departamento="TI",
            funcao="Admin",
            role="admin",
            image=None,
            status="ativo",
            senha=senha_hash
        )

        UsuarioRepository.adicionar(admin)

        print("✅ Usuário admin padrão criado")
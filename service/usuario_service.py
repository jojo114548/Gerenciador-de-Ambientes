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
         """
        Retorna a lista completa de usuários cadastrados.
        """
         return UsuarioRepository.listar()

    @staticmethod
    def cadastrar(dados):
        """
        Realiza o cadastro de um novo usuário.

        - Valida campos obrigatórios
        - Verifica duplicidade de email
        - Converte data de nascimento
        - Gera hash seguro da senha
        - Garante valores padrão para campos opcionais
        """

        # Campos mínimos exigidos para cadastro
        campos_obrigatorios = [
            "name", "email", "senha", "role", "status",
            "cpf", "data_nascimento"
        ]
        
        # Validação de campos obrigatórios
        for campo in campos_obrigatorios:
            if campo not in dados or not dados[campo]:
                raise ValueError(f"Campo obrigatório ausente: {campo}")
            
        # Verifica se já existe usuário com o mesmo email
        email_existente = UsuarioRepository.buscar_por_email(dados["email"])
        if email_existente:
            raise ValueError("Este email já está cadastrado no sistema")
        
         # Converte data de nascimento de string para date
        if dados.get("data_nascimento"):
            dados["data_nascimento"] = datetime.strptime(
                dados["data_nascimento"], "%Y-%m-%d"
            ).date()
        
        # Gera hash da senha usando bcrypt
        dados["senha"] = bcrypt.hashpw(
            dados["senha"].encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        # Garante existência de campos opcionais
        dados.setdefault("rg", None)
        dados.setdefault("telefone", None)
        dados.setdefault("endereco", None)
        dados.setdefault("departamento", None)
        dados.setdefault("funcao", None)
        dados.setdefault("image", None)

        # Cria a entidade Usuario
        users = Usuario(**dados)
        
        # Retorno reduzido por segurança
        UsuarioRepository.adicionar(users)
        
        # Retorno reduzido por segurança
        return {
            "id": users.id,
            "name": users.name,
            "email": users.email
        }

    @staticmethod
    def atualizar(usuario_id, dados):
        """
        Atualiza os dados de um usuário existente.

        - Verifica se o usuário existe
        - Remove imagem se não foi enviada
       """
        
        if not UsuarioRepository._existe(usuario_id):
            raise ValueError("Usuário não encontrado")

        # Evita sobrescrever imagem com NULL
        if "image" in dados and dados["image"] is None:
            dados.pop("image")

        UsuarioRepository.atualizar(usuario_id, dados)

    @staticmethod
    def deletar(usuario_id):
        """
        Remove um usuário do sistema a partir do ID.
        """
        if not usuario_id:
            raise ValueError("ID do usuário é obrigatório")

        UsuarioRepository.deletar(usuario_id)

    @staticmethod
    def autenticar(email, senha):
        """
        Autentica o usuário.

        - Busca usuário pelo email
        - Valida integridade do hash
        - Compara senha informada com hash do banco
        """
        usuario = UsuarioRepository.buscar_por_email(email)

        if not usuario:
            return None

        senha_hash = usuario.get("senha")

        # Proteção contra hashes inválidos no banco
        if not senha_hash or not isinstance(senha_hash, str) or not senha_hash.startswith("$2"):
            return None

        try:
            # Compara senha informada com o hash armazenado
            if bcrypt.checkpw(
                senha.encode("utf-8"),
                senha_hash.encode("utf-8")
            ):
                return usuario
        except ValueError:
            # Segurança extra caso bcrypt falhe
            return None

        return None


    # Método para o próprio usuário alterar sua senha
    @staticmethod
    def alterar_senha(usuario_id, senha_atual, senha_nova):
        """
        Permite que o próprio usuário altere sua senha.

        - Exige senha atual
        - Valida senha atual
        - Gera novo hash
        """
        if not usuario_id or not senha_atual or not senha_nova:
            raise ValueError("Todos os campos são obrigatórios")

       # Busca usuário pelo ID
        usuario = UsuarioRepository.buscar_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado")

       # Verifica se a senha atual confere
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

         # Atualiza no banco
        UsuarioRepository.atualizar_senha(usuario_id, senha_hash)


    #  Método para admin resetar senha sem precisar da senha atual
    @staticmethod
    def resetar_senha_padrao(usuario_id):
        """
        Reseta a senha para um padrão baseado no CPF.
        Exemplo: User#1234
        """

        if not usuario_id:
            raise ValueError("Usuário é obrigatório")

        usuario = UsuarioRepository.buscar_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado")

        cpf = usuario.get("cpf")

        if not cpf or len(cpf) < 4:
            raise ValueError("CPF inválido para gerar senha padrão")

         # Extrai os últimos 4 dígitos do CPF
        ultimos_4 = cpf[-4:]

        senha_padrao = f"User#{ultimos_4}"

        senha_hash = bcrypt.hashpw(
            senha_padrao.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        UsuarioRepository.atualizar_senha(usuario_id, senha_hash)

        return True
    
    @staticmethod
    def garantir_admin_padrao():
        """
        Garante a existência de um usuário administrador padrão.
        Usado normalmente na inicialização do sistema.
        """
        email_admin = "admin@nexus.com"

        # Verifica se o admin já existe
        admin_existente = UsuarioRepository.buscar_por_email(email_admin)
        if admin_existente:
            return
        

        # Gera hash da senha padrão
        senha_hash = bcrypt.hashpw(
            "Admin@123".encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")
        
         # Cria usuário administrador
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

        
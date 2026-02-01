import uuid
import bcrypt

class Usuario:
    def __init__(self,
        
        name,
        email,
        senha,
        role,
        status,
        cpf,
        rg,
        id=None,
        telefone=None,
        endereco=None,
        departamento=None,
        funcao=None,
        data_nascimento=None,
        image=None):

        self.id = id or str(uuid.uuid4())
        self.name = name
        self.email = email
        self.role = role
        self.status = status
        self.cpf = cpf
        self.rg=rg
        self.telefone = telefone
        self.endereco=endereco
        self.departamento=departamento
        self.funcao=funcao
        self.data_nascimento = data_nascimento
        self.image = image

        self.senha =senha

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "status": self.status,
            "cpf":self.cpf,
            "rg":self.rg,
            "telefone":self.telefone,
            "endereco":self.endereco,
            "departamento":self.departamento,
            "funcao":self.funcao,
            "data_nascimento":self.data_nascimento,
            "image": self.image,
            "senha": self.senha
        }

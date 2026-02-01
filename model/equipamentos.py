class Equipamento:
    def __init__(
        self,
        name,
        categoria,
        status="Disponivel",
        descricao=None,
        marca=None,
        modelo=None,
        condicao=None,
        image=None,
        especificacoes=None,
        id=None,
        created_at=None,
        quantidade_disponivel=None
    ):
        self.id = id
        self.name = name
        self.categoria = categoria
        self.status = status
        self.descricao = descricao
        self.marca = marca
        self.modelo = modelo
        self.condicao = condicao
        self.image = image
        self.created_at = created_at
        self.especificacoes = especificacoes or []
        self.quantidade_disponivel = quantidade_disponivel


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "categoria": self.categoria,
            "status": self.status,
            "descricao": self.descricao,
            "marca": self.marca,
            "modelo": self.modelo,
            "condicao": self.condicao,
            "image": self.image,
            "created_at": self.created_at,
            "especificacoes": self.especificacoes,
            "quantidade_disponivel":self.quantidade_disponivel
        }

class Ambiente:
    def __init__(
        self,
        name,
        type,
        capacidade,
        status="Disponivel",
        descricao=None,
        localizacao=None,
        area=None,
        image=None,
        recursos=None,
        id=None,
        created_at=None
    ):
        self.id = id
        self.name = name
        self.type = type
        self.capacidade = capacidade
        self.status = status
        self.descricao = descricao
        self.localizacao = localizacao
        self.area = area
        self.image = image
        self.recursos = recursos or []
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "capacidade": self.capacidade,
            "status": self.status,
            "descricao": self.descricao,
            "localizacao": self.localizacao,
            "area": self.area,
            "image": self.image,
            "recursos": self.recursos,
            "created_at": self.created_at
        }

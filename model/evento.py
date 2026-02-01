import uuid

class Evento:
    def __init__(self, titulo, data, ambiente_id, usuario_id=None, id=None):
        self.id = id or str(uuid.uuid4())
        self.titulo = titulo
        self.data = data
        self.ambiente_id = ambiente_id
        self.usuario_id = usuario_id  # quem criou

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "data": self.data,
            "ambiente_id": self.ambiente_id,
            "usuario_id": self.usuario_id
        }

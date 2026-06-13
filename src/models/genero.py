class genero:
    def __init__(self, id, nome, descricao=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao

    def __repr__(self):
        return f"<genero {self.nome}>"
class artista:
    def __init__(self, id, nome, genero_id, pais=None, descricao=None):
        self.id = id
        self.nome = nome
        self.genero_id = genero_id
        self.pais = pais
        self.descricao = descricao

    def __repr__(self):
        return f"<artista {self.nome}>"
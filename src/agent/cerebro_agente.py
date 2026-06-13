from src.repositories.historico_repositorio import WaveeDB
from src.agent.rede_bayesiana import RedeBayesiana
from src.agent.heuristica import Heuristica
from src.models.musica import musica


class CerebroAgente:
    """
    Une a Rede Bayesiana (classificação probabilística de gênero) com a
    Heuristica (ranqueamento por histórico) para decidir o que recomendar.
    """

    def __init__(self, db: WaveeDB):
        self.db = db
        self.heuristica = Heuristica()
        self._carregar_rede()

    def _carregar_rede(self):
        palavras = self.db.todas_palavras_chave()
        self.rede = RedeBayesiana(palavras)

    def classificar(self, texto: str):
        """Retorna (nome_do_genero_mais_provavel, dict_de_probabilidades)."""
        associacoes = self.db.todas_associacoes()
        return self.rede.genero_mais_provavel(texto, associacoes_extra=associacoes)

    def recomendar(self, texto: str, limite: int = 5):
        """
        Classifica o texto e retorna:
        - genero_escolhido (str)
        - probabilidades (dict)
        - lista de musicas (objetos musica) recomendadas
        """
        genero_escolhido, probabilidades = self.classificar(texto)

        linhas = self.db.musicas_por_genero(genero_escolhido, limite=limite)

        musicas = [
            musica(
                id=linha["id"],
                nome=linha["titulo"],
                genero=genero_escolhido,
                letra=None,
                cantor=linha["artista"],
            )
            for linha in linhas
        ]

        return genero_escolhido, probabilidades, musicas
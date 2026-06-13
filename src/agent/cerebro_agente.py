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

    def _montar_base_conhecimento(self):
        """
        Monta o dict {palavra: {musica_id: cliques}} a partir do histórico
        de interações no banco. Usado pela Heuristica para calcular o
        peso histórico de cada música.
        """
        base_conhecimento = {}

        for linha in self.db.historico_recente(limite=500):
            palavra = linha["entrada_texto"].strip().lower()
            musica_id = linha["musica_id"]

            if not palavra or musica_id is None or not linha["clicou"]:
                continue

            base_conhecimento.setdefault(palavra, {})
            base_conhecimento[palavra][musica_id] = (
                base_conhecimento[palavra].get(musica_id, 0) + 1
            )

        return base_conhecimento
        
    def recomendar(self, texto: str, limite: int = 5):
        """
        Classifica o texto, ranqueia as músicas do gênero escolhido usando
        a Heuristica (histórico de cliques + probabilidade bayesiana) e
        retorna:
        - genero_escolhido (str)
        - probabilidades (dict)
        - lista de musicas (objetos musica) recomendadas, ordenadas por relevância
        """
        genero_escolhido, probabilidades = self.classificar(texto)

        # busca um conjunto maior de candidatas para a heuristica ranquear
        linhas = self.db.musicas_por_genero(genero_escolhido, limite=max(limite * 3, 10))

        candidatas = [
            musica(
                id=linha["id"],
                nome=linha["titulo"],
                genero=genero_escolhido,
                letra=None,
                cantor=linha["artista"],
            )
            for linha in linhas
        ]

        base_conhecimento = self._montar_base_conhecimento()
        palavra_pesquisada = texto.strip().lower()

        candidatas.sort(
            key=lambda m: self.heuristica.calculo_final(
                m, palavra_pesquisada, base_conhecimento, probabilidades
            ),
            reverse=True,
        )

        return genero_escolhido, probabilidades, candidatas[:limite]
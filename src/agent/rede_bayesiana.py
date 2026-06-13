# Rede Bayesiana simples (Naive Bayes) para classificar o texto do usuário
# em probabilidades por gênero musical, com base nas palavras-chave do banco.

import re

# conjunto de palavras muito frequentes na língua portuguesa que normalmente
# não agregam significado relevante para a classificação do texto pela rede bayesiana.
STOPWORDS = {
    "a", "o", "os", "as",
    "de", "do", "da",
    "dos", "das",
    "e", "ou",
    "em", "no", "na",
    "nos", "nas",
    "um", "uma",
    "para", "por",
    "com", "sem"
}


class RedeBayesiana:
    def __init__(self, palavras_chave):
        """
        palavras_chave: lista de linhas do banco (palavra, peso, genero),
        como retornado por WaveeDB.todas_palavras_chave()
        """
        # tabela_pesos[genero][palavra] = peso
        self.tabela_pesos = {}

        for linha in palavras_chave:
            g = linha["genero"]
            p = linha["palavra"].lower()
            peso = linha["peso"]

            self.tabela_pesos.setdefault(
                g,
                {}
            )[p] = peso

    def _tokenizar(self, texto):

        texto = texto.lower()

        tokens = re.findall(
            r"\w+",
            texto
        )

        # remove palavras pouco informativas (stopwords),
        # preservando apenas termos relevantes para a classificação.
        tokens = [
            token
            for token in tokens
            if token not in STOPWORDS
        ]

        return tokens

    def calcular_probabilidades(
        self,
        texto,
        associacoes_extra=None
    ):
        """
        Retorna um dict {genero: probabilidade}
        normalizado (soma = 1).

        associacoes_extra: lista opcional de linhas
        (termo, peso, genero) vindas de
        associacoes_aprendidas, para reforçar a pontuação
        com base no histórico de feedback.
        """

        tokens = self._tokenizar(texto)

        pontuacao = {
            g: 0.0
            for g in self.tabela_pesos
        }

        for genero_nome, palavras in self.tabela_pesos.items():

            for token in tokens:

                if token in palavras:
                    pontuacao[genero_nome] += palavras[token]

        if associacoes_extra:

            for linha in associacoes_extra:

                termo = linha["termo"].lower()
                g = linha["genero"]

                if g in pontuacao and termo in tokens:
                    pontuacao[g] += linha["peso"]

        total = sum(
            pontuacao.values()
        )

        if total == 0:

            # sem nenhuma palavra reconhecida:
            # distribuição uniforme
            n = len(
                pontuacao
            ) or 1

            return {
                g: 1.0 / n
                for g in pontuacao
            }

        return {
            g: v / total
            for g, v in pontuacao.items()
        }

    def genero_mais_provavel(
        self,
        texto,
        associacoes_extra=None
    ):

        probs = self.calcular_probabilidades(
            texto,
            associacoes_extra
        )

        return max(
            probs,
            key=probs.get
        ), probs

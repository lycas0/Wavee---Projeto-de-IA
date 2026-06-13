from src.models.musica import musica
#onde vai ficar a lógica da heuristica
class Heuristica:
    def __init__(self, alfa = 0.6, beta = 0.4):
        # alfa = peso do histórico de cliques
        # beta = peso da probabilidade da rede bayesiana
        # alfa é maior pois, se uma palavra está fortemente associada
        # a uma música X no histórico, X tem alta chance de ser a
        # resposta desejada, e o gênero de X é consequentemente o mais provável.
        self.alfa = alfa
        self.beta = beta

    def calcular_peso_historico(self, musica_id, palavra_pesquisada, base_conhecimento): #a base conhecimento é onde vai estar guardado o historico de aprendizado, ou seja, onde vai estar guardado a relação da palavra com a letra/genero X baseado no historico de click
        """
        base_conhecimento: dict {palavra: {musica_id: cliques}}
        Retorna a proporção de cliques que essa música teve para essa palavra.
        """
        if palavra_pesquisada not in base_conhecimento:
            return 0.0
        
        click_palavra = base_conhecimento[palavra_pesquisada] #aqui vai estar as musicas que os usuarios clicaram após pesquisar uma palavra X
        total_click = sum(click_palavra.values()) #aqui a gente tá contando quantos clicks a palavra X tem relação com a musica/genero Y

        if total_click == 0: #evitando divisão por zero se a palavra não tiver nenhum click
            return 0.0

        click_musica = click_palavra.get(musica_id, 0) #aqui é a busca dos clicks na música após a pesquisa do usuario 
        return click_musica / total_click #vamos retorna a proporção que a música tem com aquela palavra 
    
#estou comentando tudo para não me perder no raciocinio 

    def calculo_final(self, musica, palavra_pesquisada, base_conhecimento, probabilidades_genero):
        """
        musica: instância de musica
        palavra_pesquisada: string usada na busca
        base_conhecimento: dict {palavra: {musica_id: cliques}}
        probabilidades_genero: dict {genero: probabilidade}, vindo da RedeBayesiana
        """
        peso_historico = self.calcular_peso_historico(
            musica.id, palavra_pesquisada, base_conhecimento
        )

        peso_bayesiano = probabilidades_genero.get(musica.genero, 0.0)

        return (self.alfa * peso_historico) + (self.beta * peso_bayesiano)
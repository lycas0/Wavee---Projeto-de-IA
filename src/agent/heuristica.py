from src.models.musica import musica
#onde vai ficar a lógica da heuristica
class Heuristica:
    def __init__(self, alfa = 0.6, beta = 0.4):
        #aqui vai estar os pesos da nossa busca, que nesse caso vai ser o alfa = peso_historico e beta = peso_rede_bayesiana
        #o peso alfa tem mais valor pois se uma determinada palavra é muito associada a uma música X, sempre que essa palavra estiver na pesquisa do usuário a música X tem maiores probabilidades de ser a música desejada e assim o gênero musical dessa música é consequentemente o mais provavel
        self.alfa = alfa
        self.beta = beta

    def calcular_peso_historico(self, musica_id, palavra_pesquisada, base_conhecimento): #a base conhecimento é onde vai estar guardado o historico de aprendizado, ou seja, onde vai estar guardado a relação da palavra com a letra/genero X baseado no historico de click

        if palavra_pesquisada not in base_conhecimento:
            return 0.0
        
        click_palavra = base_conhecimento[palavra_pesquisada] #aqui vai estar as musicas que os usuarios clicaram após pesquisar uma palavra X
        total_click = sum(click_palavra.values()) #aqui a gente tá contando quantos clicks a palavra X tem relação com a musica/genero Y

        if total_click == 0: #evitando divisão por zero se a palavra não tiver nenhum click
            return 0.0

        click_musica = click_palavra.get(musica_id, 0) #aqui é a busca dos clicks na música após a pesquisa do usuario 

        return click_musica / total_click #vamos retorna a proporção que a música tem com aquela palavra 
    
#estou comentando tudo para não me perder no raciocinio 

    def calculo_final(self, musica: musica, palavra_pesquisada, base_conhecimento, rede_bayesiana):
        
        idMusica = musica.id
        generoMusica = musica.genero

        pesoHistorico = self.calcular_peso_historico(idMusica, palavra_pesquisada, base_conhecimento)

        #pesoBayesiano = aqui vamos receber a probabilidade gerada pela rede bayesiana

        #resultadoFinal = (self.alfa * pesoHistorico) + (self.beta * pesoBayesiano)

        #return resultadoFinal

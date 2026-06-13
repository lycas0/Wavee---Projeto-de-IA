import tkinter as tk
from tkinter import messagebox


class AppWindow:

    def __init__(self):

        # cria a janela principal que servirá como ponto de interação entre o usuário e o sistema de recomendação musical.
        self.janela = tk.Tk()

        # define o nome exibido na barra superior da aplicação.
        self.janela.title("Wavee")

        # define o tamanho inicial da interface.
        self.janela.geometry("700x500")

        # centraliza a criação dos componentes visuais em um único método.
        self.criar_componentes()

    def criar_componentes(self):

        # identidade visual da aplicação. facilita o reconhecimento da ferramenta pelo usuário.
        titulo = tk.Label(
            self.janela,
            text="🎵 Wavee",
            font=("Arial", 20)
        )

        titulo.pack(pady=10)

        # campo onde o usuário poderá informar uma letra de música ou descrever seus gostos musicais para análise.
        self.campo_texto = tk.Text(
            self.janela,
            height=6,
            width=60
        )

        self.campo_texto.pack()

        # dispara o processo de inferência. quando clicado, o texto será coletado e enviado para análise.
        botao = tk.Button(
            self.janela,
            text="Buscar",
            command=self.buscar
        )

        botao.pack(pady=10)

        # área reservada para exibir o resultado retornado pela ia. inicialmente permanece vazia até que uma busca seja realizada.
        self.resultado = tk.Label(
            self.janela,
            text=""
        )

        self.resultado.pack()

    def buscar(self):

        # recupera todo o conteúdo digitado pelo usuário no campo de texto.
        texto = self.campo_texto.get(
            "1.0",
            tk.END
        )

        # placeholder temporário. futuramente essa variável receberá a resposta da rede bayesiana.
        genero = "Rock"

        # atualiza a interface com o gênero identificado, fornecendo feedback imediato ao usuário.
        self.resultado.config(
            text=f"Gênero identificado: {genero}"
        )

    def executar(self):

        # mantém a aplicação em execução aguardando interações do usuário até que a janela seja encerrada.
        self.janela.mainloop()
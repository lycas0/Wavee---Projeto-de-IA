import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class AppWindow:

    def __init__(self):

        # cria a janela principal da aplicação
        self.janela = tk.Tk()

        self.janela.title("Wavee")

        # tamanho inicial da janela
        self.janela.geometry("800x700")

        # cor de fundo inspirada na identidade visual
        self.janela.configure(bg="#0f1117")

        self.criar_componentes()

    def criar_componentes(self):

        # logo do wavee

        imagem = Image.open("assets/logo_wavee.png")

        imagem = imagem.resize((220, 220))

        self.logo = ImageTk.PhotoImage(imagem)

        logo_label = tk.Label(
            self.janela,
            image=self.logo,
            bg="#0f1117"
        )

        logo_label.pack(pady=10)

        # título

        titulo = tk.Label(
            self.janela,
            text="Seu assistente musical inteligente",
            font=("Arial", 14, "bold"),
            bg="#0f1117",
            fg="#65f0c4"
        )

        titulo.pack()

        # subtítulo

        subtitulo = tk.Label(
            self.janela,
            text="Descubra músicas com Inteligência Artificial",
            font=("Arial", 10),
            bg="#0f1117",
            fg="white"
        )

        subtitulo.pack(pady=(0, 20))

        # instrução

        instrucao = tk.Label(
            self.janela,
            text="Digite uma letra de música ou descreva seu gosto musical:",
            font=("Arial", 11),
            bg="#0f1117",
            fg="white"
        )

        instrucao.pack()

        # campo de texto

        self.campo_texto = tk.Text(
            self.janela,
            height=6,
            width=60,
            font=("Arial", 11)
        )

        self.campo_texto.pack(pady=10)

        # botão de busca

        botao = tk.Button(
            self.janela,
            text="Buscar",
            command=self.buscar,
            bg="#65f0c4",
            font=("Arial", 11, "bold")
        )

        botao.pack(pady=10)

        # resultado

        self.resultado = tk.Label(
            self.janela,
            text="",
            font=("Arial", 12),
            bg="#0f1117",
            fg="white"
        )

        self.resultado.pack(pady=20)

    def buscar(self):

        texto = self.campo_texto.get(
            "1.0",
            tk.END
        )

        if not texto.strip():

            messagebox.showwarning(
                "Aviso",
                "Digite algum texto para análise."
            )

            return

        # placeholder temporário
        # aqui será integrada a rede bayesiana

        genero = "Rock"

        self.resultado.config(
            text=f"Gênero identificado: {genero}"
        )

    def executar(self):

        self.janela.mainloop()

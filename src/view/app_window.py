import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from src.agent.agente import Agente


class AppWindow:

    def __init__(self):

        # cria a janela principal da aplicação
        self.janela = tk.Tk()

        # cria o agente inteligente
        self.agente = Agente()

        self.janela.title("Wavee")

        # tamanho da janela
        self.janela.geometry("800x700")

        # cor extraída do fundo da logo
        self.janela.configure(bg="#0C0C0E")

        self.criar_componentes()

    def criar_componentes(self):

        # logo do wavee

        imagem = Image.open("assets/logo_wavee.png")

        imagem = imagem.resize((220, 220))

        self.logo = ImageTk.PhotoImage(imagem)

        logo_label = tk.Label(
            self.janela,
            image=self.logo,
            bg="#0C0C0E"
        )

        logo_label.pack(pady=(20, 5))

        # slogan

        subtitulo = tk.Label(
            self.janela,
            text="O agente inteligente que entende seu ritmo",
            font=("Arial", 12),
            bg="#0C0C0E",
            fg="#9CEACD"
        )

        subtitulo.pack(pady=(0, 30))

        # instrução

        instrucao = tk.Label(
            self.janela,
            text="Digite uma letra de música ou descreva seu gosto musical",
            font=("Arial", 11),
            bg="#0C0C0E",
            fg="white"
        )

        instrucao.pack()

        # campo de texto

        self.campo_texto = tk.Text(
            self.janela,
            height=5,
            width=55,
            font=("Arial", 11),
            relief="flat"
        )

        self.campo_texto.pack(pady=15)

        # botão de busca

        botao = tk.Button(
            self.janela,
            text="Buscar",
            command=self.buscar,
            bg="#9CEACD",
            fg="#0C0C0E",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=5,
            borderwidth=0
        )

        botao.pack(pady=10)

        # separador

        separador = tk.Frame(
            self.janela,
            bg="#2A2A2D",
            height=2,
            width=500
        )

        separador.pack(pady=25)

        # resultado

        self.resultado = tk.Label(
            self.janela,
            text="🎧 Gênero identificado:",
            font=("Arial", 13, "bold"),
            bg="#0C0C0E",
            fg="white"
        )

        self.resultado.pack()

        # recomendações

        self.recomendacoes = tk.Label(
            self.janela,
            text="",
            font=("Arial", 11),
            bg="#0C0C0E",
            fg="white",
            justify="left"
        )

        self.recomendacoes.pack(pady=15)

    def buscar(self):

        texto = self.campo_texto.get(
            "1.0",
            tk.END
        ).strip()

        if not texto:

            messagebox.showwarning(
                "Aviso",
                "Digite algum texto para análise."
            )

            return

        try:

            resultado = self.agente.agir(texto)

            genero = resultado["genero"]

            musicas = resultado["musicas"]

            self.resultado.config(
                text=f"🎧 Gênero identificado: {genero}"
            )

            texto_musicas = "🎵 Músicas recomendadas:\n\n"

            for musica in musicas:

                texto_musicas += (
                    f"• {musica.nome} "
                    f"({musica.cantor})\n"
                )

            self.recomendacoes.config(
                text=texto_musicas
            )

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                f"Ocorreu um erro:\n\n{erro}"
            )

    def executar(self):

        self.janela.mainloop()
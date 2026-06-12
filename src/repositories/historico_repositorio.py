import sqlite3
import os
from typing import Optional

DB_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "wavee.db"
)


class WaveeDB:
    """Conexão única com o banco. Instancie uma vez e reutilize."""

    def __init__(self, db_path: str = DB_PATH):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row          # linhas acessíveis por nome
        self.conn.execute("PRAGMA foreign_keys = ON")


    def todos_generos(self) -> list[sqlite3.Row]:
        """Retorna todos os gêneros cadastrados."""
        return self.conn.execute("SELECT * FROM generos ORDER BY nome").fetchall()

    def genero_por_id(self, genero_id: int) -> Optional[sqlite3.Row]:
        return self.conn.execute(
            "SELECT * FROM generos WHERE id = ?", (genero_id,)
        ).fetchone()

    def genero_por_nome(self, nome: str) -> Optional[sqlite3.Row]:
        return self.conn.execute(
            "SELECT * FROM generos WHERE nome = ?", (nome,)
        ).fetchone()


    def palavras_por_genero(self, genero_id: int) -> list[sqlite3.Row]:
        """Retorna palavras-chave e seus pesos para um gênero específico."""
        return self.conn.execute(
            "SELECT palavra, peso FROM palavras_chave WHERE genero_id = ?",
            (genero_id,),
        ).fetchall()

    def todas_palavras_chave(self) -> list[sqlite3.Row]:
        """
        Retorna todas as palavras-chave com o nome do gênero associado.
        Útil para construir a tabela de probabilidades do agente.
        """
        return self.conn.execute(
            """SELECT pc.palavra, pc.peso, g.nome AS genero
               FROM palavras_chave pc
               JOIN generos g ON g.id = pc.genero_id
               ORDER BY g.nome, pc.peso DESC"""
        ).fetchall()

    def artistas_por_genero(self, genero_id: int) -> list[sqlite3.Row]:
        return self.conn.execute(
            "SELECT * FROM artistas WHERE genero_id = ? ORDER BY nome",
            (genero_id,),
        ).fetchall()


    def musicas_por_genero(self, genero_nome: str, limite: int = 5) -> list[sqlite3.Row]:
        """
        Retorna até `limite` músicas de um gênero, com dados do artista incluídos.
        É a principal chamada feita pelo agente após classificar o gênero.
        """
        return self.conn.execute(
            """SELECT m.id, m.titulo, m.album, m.ano, m.duracao_seg, m.url_preview,
                      a.nome AS artista, g.nome AS genero
               FROM musicas m
               JOIN artistas a ON a.id = m.artista_id
               JOIN generos  g ON g.id = m.genero_id
               WHERE g.nome = ?
               ORDER BY RANDOM()
               LIMIT ?""",
            (genero_nome, limite),
        ).fetchall()

    def musicas_por_genero_id(self, genero_id: int, limite: int = 5) -> list[sqlite3.Row]:
        """Igual ao método anterior, mas recebe o ID em vez do nome."""
        return self.conn.execute(
            """SELECT m.id, m.titulo, m.album, m.ano, m.duracao_seg, m.url_preview,
                      a.nome AS artista, g.nome AS genero
               FROM musicas m
               JOIN artistas a ON a.id = m.artista_id
               JOIN generos  g ON g.id = m.genero_id
               WHERE m.genero_id = ?
               ORDER BY RANDOM()
               LIMIT ?""",
            (genero_id, limite),
        ).fetchall()

    def buscar_musica(self, titulo: str) -> list[sqlite3.Row]:
        """Busca músicas cujo título contenha o termo informado."""
        return self.conn.execute(
            """SELECT m.*, a.nome AS artista, g.nome AS genero
               FROM musicas m
               JOIN artistas a ON a.id = m.artista_id
               JOIN generos  g ON g.id = m.genero_id
               WHERE m.titulo LIKE ?""",
            (f"%{titulo}%",),
        ).fetchall()
    
    def registrar_interacao(
        self,
        entrada_texto: str,
        genero_id: Optional[int] = None,
        musica_id: Optional[int] = None,
        clicou: bool = False,
        feedback: Optional[int] = None,
    ) -> int:
        """
        Salva uma interação do usuário.

        feedback: 1 = gostou, -1 = não gostou, None = sem resposta
        Retorna o ID da linha inserida.
        """
        cur = self.conn.execute(
            """INSERT INTO historico (entrada_texto, genero_id, musica_id, clicou, feedback)
               VALUES (?,?,?,?,?)""",
            (entrada_texto, genero_id, musica_id, int(clicou), feedback),
        )
        self.conn.commit()
        return cur.lastrowid

    def historico_recente(self, limite: int = 50) -> list[sqlite3.Row]:
        """Últimas interações registradas."""
        return self.conn.execute(
            """SELECT h.*, g.nome AS genero, m.titulo AS musica
               FROM historico h
               LEFT JOIN generos g ON g.id = h.genero_id
               LEFT JOIN musicas m ON m.id = h.musica_id
               ORDER BY h.criado_em DESC
               LIMIT ?""",
            (limite,),
        ).fetchall()

    def feedback_por_genero(self) -> list[sqlite3.Row]:
        """
        Agrega feedback positivo e negativo por gênero.
        Útil para ajustar pesos do modelo com o tempo.
        """
        return self.conn.execute(
            """SELECT g.nome AS genero,
                      SUM(CASE WHEN h.feedback =  1 THEN 1 ELSE 0 END) AS positivos,
                      SUM(CASE WHEN h.feedback = -1 THEN 1 ELSE 0 END) AS negativos,
                      SUM(h.clicou) AS total_cliques
               FROM historico h
               JOIN generos g ON g.id = h.genero_id
               GROUP BY g.nome
               ORDER BY positivos DESC"""
        ).fetchall()


    def registrar_associacao(self, termo: str, genero_id: int, peso_incremento: float = 0.1):
        """
        Registra ou reforça a associação entre um termo e um gênero.

        Se a associação já existir, incrementa o peso e a contagem de ocorrências.
        Chamado automaticamente quando o usuário dá feedback positivo.
        """
        self.conn.execute(
            """INSERT INTO associacoes_aprendidas (termo, genero_id, peso, ocorrencias, ultima_vez)
               VALUES (?, ?, ?, 1, datetime('now'))
               ON CONFLICT(termo, genero_id) DO UPDATE SET
                   peso       = MIN(peso + ?, 5.0),
                   ocorrencias = ocorrencias + 1,
                   ultima_vez = datetime('now')""",
            (termo, genero_id, 1.0 + peso_incremento, peso_incremento),
        )
        self.conn.commit()

    def associacoes_por_genero(self, genero_id: int) -> list[sqlite3.Row]:
        """Retorna todas as associações aprendidas para um gênero, ordenadas por peso."""
        return self.conn.execute(
            """SELECT termo, peso, ocorrencias, ultima_vez
               FROM associacoes_aprendidas
               WHERE genero_id = ?
               ORDER BY peso DESC""",
            (genero_id,),
        ).fetchall()

    def buscar_associacao(self, termo: str) -> list[sqlite3.Row]:
        """
        Busca em quais gêneros um termo foi aprendido.
        Usado pelo agente para enriquecer a classificação Naive Bayes.
        """
        return self.conn.execute(
            """SELECT a.termo, a.peso, a.ocorrencias, g.nome AS genero
               FROM associacoes_aprendidas a
               JOIN generos g ON g.id = a.genero_id
               WHERE a.termo LIKE ?
               ORDER BY a.peso DESC""",
            (f"%{termo}%",),
        ).fetchall()

    def todas_associacoes(self) -> list[sqlite3.Row]:
        """Retorna todas as associações aprendidas — útil para recarregar o modelo."""
        return self.conn.execute(
            """SELECT a.termo, a.peso, a.ocorrencias, g.nome AS genero
               FROM associacoes_aprendidas a
               JOIN generos g ON g.id = a.genero_id
               ORDER BY g.nome, a.peso DESC"""
        ).fetchall()


    def estatisticas(self) -> dict:
        """Resumo rápido do conteúdo do banco."""
        def count(tabela):
            return self.conn.execute(f"SELECT COUNT(*) FROM {tabela}").fetchone()[0]

        return {
            "generos":               count("generos"),
            "palavras_chave":        count("palavras_chave"),
            "artistas":              count("artistas"),
            "musicas":               count("musicas"),
            "associacoes_aprendidas":count("associacoes_aprendidas"),
            "historico":             count("historico"),
        }

    def fechar(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.fechar()
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "wavee.db")


CREATE_TABLES = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS generos (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    nome      TEXT    NOT NULL UNIQUE,           
    descricao TEXT                               
);

CREATE TABLE IF NOT EXISTS palavras_chave (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    genero_id INTEGER NOT NULL REFERENCES generos(id) ON DELETE CASCADE,
    palavra   TEXT    NOT NULL,
    peso      REAL    NOT NULL DEFAULT 1.0       
);

CREATE TABLE IF NOT EXISTS artistas (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    nome       TEXT    NOT NULL UNIQUE,
    genero_id  INTEGER REFERENCES generos(id),   
    pais       TEXT,
    descricao  TEXT
);

CREATE TABLE IF NOT EXISTS musicas (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo      TEXT    NOT NULL,
    artista_id  INTEGER NOT NULL REFERENCES artistas(id) ON DELETE CASCADE,
    genero_id   INTEGER NOT NULL REFERENCES generos(id),
    album       TEXT,
    ano         INTEGER,
    duracao_seg INTEGER,                         
    url_preview TEXT                             
);

CREATE TABLE IF NOT EXISTS associacoes_aprendidas (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    termo          TEXT    NOT NULL,                  -- palavra ou expressão aprendida
    genero_id      INTEGER NOT NULL REFERENCES generos(id) ON DELETE CASCADE,
    peso           REAL    NOT NULL DEFAULT 1.0,      -- força da associação (aumenta com feedback positivo)
    ocorrencias    INTEGER NOT NULL DEFAULT 1,        -- quantas vezes esse termo gerou feedback positivo
    ultima_vez     TEXT    NOT NULL DEFAULT (datetime('now')), -- última atualização
    UNIQUE(termo, genero_id)                          -- um termo não se repete para o mesmo gênero
);

CREATE TABLE IF NOT EXISTS historico (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    entrada_texto TEXT   NOT NULL,               -- texto que o usuário digitou
    genero_id    INTEGER REFERENCES generos(id), -- gênero classificado pelo agente
    musica_id    INTEGER REFERENCES musicas(id), -- música que foi recomendada
    clicou       INTEGER NOT NULL DEFAULT 0,     -- 1 = clicou, 0 = ignorou
    feedback     INTEGER,                        -- 1 = positivo, -1 = negativo, NULL = sem feedback
    criado_em    TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_palavras_genero      ON palavras_chave(genero_id);
CREATE INDEX IF NOT EXISTS idx_associacoes_termo    ON associacoes_aprendidas(termo);
CREATE INDEX IF NOT EXISTS idx_associacoes_genero   ON associacoes_aprendidas(genero_id);
CREATE INDEX IF NOT EXISTS idx_musicas_genero    ON musicas(genero_id);
CREATE INDEX IF NOT EXISTS idx_musicas_artista   ON musicas(artista_id);
CREATE INDEX IF NOT EXISTS idx_historico_entrada ON historico(entrada_texto);
CREATE INDEX IF NOT EXISTS idx_historico_musica  ON historico(musica_id);
"""


GENEROS = [
    ("Pop",        "Músicas populares de apelo amplo, melodias cativantes e letras simples."),
    ("Rock",       "Guitarra elétrica, bateria forte e energia intensa."),
    ("Sertanejo",  "Música country brasileira, duplas, amor e saudade do campo."),
    ("Funk",       "Batidas pesadas de baile, letras urbanas, originário do Rio de Janeiro."),
    ("MPB",        "Música Popular Brasileira, sofisticação harmônica e letras poéticas."),
    ("Hip-Hop",    "Rimas, beats, cultura de rua e narrativa urbana."),
    ("Eletrônica", "Produção digital, sintetizadores, dancefloor e festivais."),
    ("Forró",      "Ritmo nordestino, sanfona, zabumba e triângulo."),
    ("Pagode",     "Samba urbano, pandeiro, afeto e alegria carioca."),
    ("Metal",      "Guitarras distorcidas, vocais agressivos, complexidade técnica."),
]

PALAVRAS_CHAVE = [
    ("Pop", "amor",        1.5), ("Pop", "dança",       1.3), ("Pop", "hit",         1.2),
    ("Pop", "melodia",     1.2), ("Pop", "pop",         2.0), ("Pop", "radio",       1.1),
    ("Pop", "coro",        1.0), ("Pop", "verão",       1.1), ("Pop", "festa",       1.2),
    ("Pop", "romântico",   1.1),

    ("Rock", "guitarra",   2.0), ("Rock", "bateria",    1.8), ("Rock", "rock",       2.0),
    ("Rock", "banda",      1.3), ("Rock", "distorção",  1.5), ("Rock", "solo",       1.4),
    ("Rock", "rebeldia",   1.2), ("Rock", "energia",    1.1), ("Rock", "pesado",     1.3),
    ("Rock", "riff",       1.6),

    ("Sertanejo", "sertanejo", 2.0), ("Sertanejo", "dupla",     1.8),
    ("Sertanejo", "viola",     1.7), ("Sertanejo", "saudade",   1.4),
    ("Sertanejo", "campo",     1.3), ("Sertanejo", "boiadeiro", 1.5),
    ("Sertanejo", "coração",   1.1), ("Sertanejo", "country",   1.6),
    ("Sertanejo", "interior",  1.2), ("Sertanejo", "fazenda",   1.4),

    ("Funk", "funk",      2.0), ("Funk", "baile",     1.8), ("Funk", "batida",    1.6),
    ("Funk", "favela",    1.4), ("Funk", "proibido",  1.3), ("Funk", "carioca",   1.5),
    ("Funk", "ostentação",1.3), ("Funk", "mc",        1.7), ("Funk", "grave",     1.2),
    ("Funk", "pancadão",  1.5),

    ("MPB", "mpb",        2.0), ("MPB", "bossa",      1.8), ("MPB", "poesia",     1.7),
    ("MPB", "brasil",     1.3), ("MPB", "violão",     1.5), ("MPB", "saudade",    1.2),
    ("MPB", "voz",        1.1), ("MPB", "letra",      1.4), ("MPB", "clássico",   1.3),
    ("MPB", "autoral",    1.5),

    ("Hip-Hop", "rap",      2.0), ("Hip-Hop", "rima",     1.9), ("Hip-Hop", "flow",     1.8),
    ("Hip-Hop", "beat",     1.6), ("Hip-Hop", "verso",    1.5), ("Hip-Hop", "sample",   1.4),
    ("Hip-Hop", "periferia",1.5), ("Hip-Hop", "trap",     1.4), ("Hip-Hop", "freestyle",1.6),
    ("Hip-Hop", "skate",    1.1),

    ("Eletrônica", "eletrônico", 2.0), ("Eletrônica", "sintetizador", 1.8),
    ("Eletrônica", "dj",         1.7), ("Eletrônica", "festival",     1.5),
    ("Eletrônica", "drop",       1.6), ("Eletrônica", "loop",         1.4),
    ("Eletrônica", "techno",     1.5), ("Eletrônica", "house",        1.5),
    ("Eletrônica", "bass",       1.3), ("Eletrônica", "remix",        1.4),

    ("Forró", "forró",      2.0), ("Forró", "sanfona",   1.9), ("Forró", "nordeste",  1.7),
    ("Forró", "zabumba",    1.8), ("Forró", "triângulo", 1.7), ("Forró", "pé-de-serra",1.6),
    ("Forró", "arrasta-pé", 1.5), ("Forró", "caatinga",  1.3), ("Forró", "xote",      1.6),
    ("Forró", "baião",      1.7),
    
    ("Pagode", "pagode",    2.0), ("Pagode", "samba",     1.8), ("Pagode", "pandeiro",  1.7),
    ("Pagode", "cavaquinho",1.7), ("Pagode", "roda",      1.4), ("Pagode", "Rio",       1.2),
    ("Pagode", "alegria",   1.2), ("Pagode", "boteco",    1.5), ("Pagode", "amizade",   1.1),
    ("Pagode", "choro",     1.4),
    
    ("Metal", "metal",      2.0), ("Metal", "heavy",     1.8), ("Metal", "thrash",    1.7),
    ("Metal", "death",      1.6), ("Metal", "power",     1.5), ("Metal", "riff",      1.6),
    ("Metal", "breakdown",  1.5), ("Metal", "headbang",  1.4), ("Metal", "distorção", 1.4),
    ("Metal", "vocal gutural", 1.7),
]

ARTISTAS = [
    ("Taylor Swift",      "Pop",        "EUA",    "Uma das maiores artistas pop da atualidade."),
    ("The Beatles",       "Rock",       "Reino Unido", "Banda mais influente da história do rock."),
    ("Legião Urbana",     "Rock",       "Brasil", "Ícone do rock nacional, letras poéticas."),
    ("Jorge & Mateus",    "Sertanejo",  "Brasil", "Dupla sertaneja universitária de sucesso."),
    ("Anitta",            "Pop",        "Brasil", "Cantora pop brasileira de projeção mundial."),
    ("MC Livinho",        "Funk",       "Brasil", "MC funk de grande popularidade no Brasil."),
    ("Caetano Veloso",    "MPB",        "Brasil", "Ícone da MPB e do movimento Tropicália."),
    ("Gilberto Gil",      "MPB",        "Brasil", "Músico e poeta, ex-ministro da Cultura."),
    ("Emicida",           "Hip-Hop",    "Brasil", "Rapper paulistano, voz da periferia."),
    ("Criolo",            "Hip-Hop",    "Brasil", "Rapper e músico de São Paulo, múltiplos gêneros."),
    ("Martin Garrix",     "Eletrônica", "Holanda","DJ e produtor de EDM, recordista no Spotify."),
    ("Dua Lipa",          "Pop",        "Reino Unido", "Artista pop com influências disco e eletrônicas."),
    ("Luiz Gonzaga",      "Forró",      "Brasil", "Rei do Baião, símbolo do nordeste brasileiro."),
    ("Dominguinhos",      "Forró",      "Brasil", "Sanfoneiro virtuoso do forró e do choro."),
    ("Exaltasamba",       "Pagode",     "Brasil", "Grupo de pagode carioca de grande sucesso."),
    ("Thiaguinho",        "Pagode",     "Brasil", "Cantor de pagode e samba romântico."),
    ("Sepultura",         "Metal",      "Brasil", "Uma das bandas de metal mais famosas do mundo."),
    ("Metallica",         "Metal",      "EUA",    "Banda de thrash metal mais bem-sucedida da história."),
    ("Beyoncé",           "Pop",        "EUA",    "Artista pop e R&B de impacto global."),
    ("Zé Neto & Cristiano","Sertanejo", "Brasil", "Dupla sertaneja conhecida pelas letras românticas."),
]

MUSICAS = [
    ("Shake It Off",        "Taylor Swift",   "Pop",        "1989",                  2014, 219, "https://open.spotify.com/track/0cqRj7pUJDkTCEsJkx8snD"),
    ("Blank Space",         "Taylor Swift",   "Pop",        "1989",                  2014, 231, "https://open.spotify.com/track/06HL4z0CvFAxyc27GXpf02"),
    ("Come Together",       "The Beatles",    "Rock",       "Abbey Road",            1969, 259, "https://open.spotify.com/track/2EqlS6tkEnglzr7tkKAAYh"),
    ("Let It Be",           "The Beatles",    "Rock",       "Let It Be",             1970, 243, "https://open.spotify.com/track/7iN1s7xHE4ifF5povM6A48"),
    ("Tempo Perdido",       "Legião Urbana",  "Rock",       "Dois",                  1986, 320, "https://open.spotify.com/track/2s6VNnFkm6VEMFoMJoMBi2"),
    ("Há Tempos",           "Legião Urbana",  "Rock",       "V",                     1991, 259, "https://open.spotify.com/track/43K2iuaFWbsTfMKsIpF1w4"),
    ("O Combate",           "Jorge & Mateus", "Sertanejo",  "Só Os Dois",            2010, 212, None),
    ("No Dia que Eu Saí de Casa", "Jorge & Mateus","Sertanejo","Ao Vivo em Goiânia", 2010, 270, None),
    ("Vai Malandra",        "Anitta",         "Funk",       "Vai Malandra",          2017, 178, "https://open.spotify.com/track/3gUQWlBoFyDYXBjjFPXFIL"),
    ("Downtown",            "Anitta",         "Pop",        "Kisses",                2019, 195, "https://open.spotify.com/track/5HxRHSKIJvSNQGE3JXs3OB"),
    ("Aquele 1%",           "MC Livinho",     "Funk",       "Single",                2016, 190, None),
    ("Sozinho",             "Caetano Veloso", "MPB",        "Livro",                 1997, 238, "https://open.spotify.com/track/1eREE3j3bCCNqBKbcMDJxU"),
    ("Domingo no Parque",   "Gilberto Gil",   "MPB",        "Gilberto Gil",          1967, 195, None),
    ("Triste, Louca ou Má", "Emicida",        "Hip-Hop",    "Sobre Crianças...",     2015, 268, "https://open.spotify.com/track/5lmBZNqJqTdPoLWBDIEkHQ"),
    ("Nó na Orelha",        "Criolo",         "Hip-Hop",    "Nó na Orelha",          2011, 221, None),
    ("Animals",             "Martin Garrix",  "Eletrônica", "Animals",               2013, 245, "https://open.spotify.com/track/47wkHZBliKjFMYBt0BF3Na"),
    ("Levitating",          "Dua Lipa",       "Pop",        "Future Nostalgia",      2020, 203, "https://open.spotify.com/track/463CkQjx2Zfoiqr0ESdVHm"),
    ("Asa Branca",          "Luiz Gonzaga",   "Forró",      "Asa Branca",            1947, 172, None),
    ("Baião",               "Dominguinhos",   "Forró",      "Sanfoneiro de Ouro",    1988, 165, None),
    ("Tô Nem Aí",           "Exaltasamba",    "Pagode",     "Espelho",               2004, 230, None),
    ("Deixa a Vida Me Levar","Thiaguinho",    "Pagode",     "Ousadia & Alegria",     2012, 215, None),
    ("Roots Bloody Roots",  "Sepultura",      "Metal",      "Roots",                 1996, 256, "https://open.spotify.com/track/28PsJOTrfWtOzHvDLb0GJ9"),
    ("Enter Sandman",       "Metallica",      "Metal",      "Metallica (Black Album)",1991, 331, "https://open.spotify.com/track/2TjdnqlpwOjhijHCwHCP2d"),
    ("Crazy in Love",       "Beyoncé",        "Pop",        "Dangerously in Love",   2003, 236, "https://open.spotify.com/track/5IVuqXILoxVWvWEPm82Jxr"),
    ("Para de Marra",       "Zé Neto & Cristiano","Sertanejo","Dois Caipiras",       2018, 198, None),
]


def popular_banco(cur: sqlite3.Cursor):
    genero_ids: dict[str, int] = {}
    for nome, desc in GENEROS:
        cur.execute("INSERT OR IGNORE INTO generos (nome, descricao) VALUES (?,?)", (nome, desc))
        cur.execute("SELECT id FROM generos WHERE nome = ?", (nome,))
        genero_ids[nome] = cur.fetchone()[0]

    for g_nome, palavra, peso in PALAVRAS_CHAVE:
        cur.execute(
            "INSERT INTO palavras_chave (genero_id, palavra, peso) VALUES (?,?,?)",
            (genero_ids[g_nome], palavra, peso),
        )

    artista_ids: dict[str, int] = {}
    for nome, g_nome, pais, desc in ARTISTAS:
        cur.execute(
            "INSERT OR IGNORE INTO artistas (nome, genero_id, pais, descricao) VALUES (?,?,?,?)",
            (nome, genero_ids[g_nome], pais, desc),
        )
        cur.execute("SELECT id FROM artistas WHERE nome = ?", (nome,))
        artista_ids[nome] = cur.fetchone()[0]

    for titulo, a_nome, g_nome, album, ano, dur, url in MUSICAS:
        cur.execute(
            """INSERT INTO musicas (titulo, artista_id, genero_id, album, ano, duracao_seg, url_preview)
               VALUES (?,?,?,?,?,?,?)""",
            (titulo, artista_ids[a_nome], genero_ids[g_nome], album, ano, dur, url),
        )

    print(f"  {len(GENEROS)} gêneros inseridos")
    print(f"  {len(PALAVRAS_CHAVE)} palavras-chave inseridas")
    print(f"  {len(ARTISTAS)} artistas inseridos")
    print(f"  {len(MUSICAS)} músicas inseridas")


def main():
    db_exists = os.path.exists(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript(CREATE_TABLES)

    if db_exists:
        print("wavee.db já existe. Recriando dados...")
        cur.executescript("""
            DELETE FROM historico;
            DELETE FROM musicas;
            DELETE FROM artistas;
            DELETE FROM palavras_chave;
            DELETE FROM generos;
        """)

    print("Populando banco de dados Wavee...")
    popular_banco(cur)
    conn.commit()
    conn.close()
    print(f"Banco criado com sucesso em: {DB_PATH}")


if __name__ == "__main__":
    main()
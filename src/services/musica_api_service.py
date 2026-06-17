"""
music_api_service.py — Integração com a API do Spotify para o Wavee.

Responsável por:
- Autenticar com a API do Spotify (Client Credentials Flow)
- Buscar músicas, artistas e gêneros por categoria
- Importar e persistir os dados no banco SQLite
- Validar integridade antes de salvar

Uso:
    python src/services/music_api_service.py
"""

import requests
import base64
import sqlite3
import os
import time


CLIENT_ID     = "4acd9f7e0e874aba841abcff7d0d1bad"
CLIENT_SECRET = "c146291222244a84b6c55d26955aa43f"

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "wavee.db")

GENEROS_BUSCA = {
    "Rock":       ["rock brasileiro", "classic rock", "rock nacional"],
    "Pop":        ["pop brasil", "pop internacional"],
    "Sertanejo":  ["sertanejo universitário", "sertanejo romântico"],
    "Funk":       ["funk carioca", "funk brasileiro"],
    "MPB":        ["MPB", "bossa nova brasileira"],
    "Hip-Hop":    ["rap brasileiro", "hip hop nacional"],
    "Eletrônica": ["eletrônica brasil", "EDM"],
    "Forró":      ["forró pé de serra", "forró eletrônico"],
    "Pagode":     ["pagode brasileiro", "samba pagode"],
    "Metal":      ["metal brasileiro", "heavy metal"],
}

LIMITE_POR_GENERO = 10


def obter_token() -> str:
    """
    Autentica via Client Credentials Flow e retorna o access token.
    Não requer login do usuário — perfeito para importação de dados.
    """
    creds = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    resposta = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={"Authorization": f"Basic {creds}"},
        data={"grant_type": "client_credentials"},
        timeout=10,
    )

    if resposta.status_code != 200:
        raise Exception(f"Erro ao autenticar: {resposta.status_code} — {resposta.text}")

    token = resposta.json().get("access_token")
    print("✓ Autenticado no Spotify com sucesso.")
    return token


def buscar_musicas(token: str, query: str, limite: int = 10) -> list[dict]:
    """
    Busca músicas no Spotify por termo/gênero.
    Retorna lista de dicts com título, artista, álbum, ano e URL de preview.
    """
    headers = {"Authorization": f"Bearer {token}"}
    params  = {"q": query, "type": "track", "market": "BR", "limit": limite}

    resposta = requests.get(
        "https://api.spotify.com/v1/search",
        headers=headers,
        params=params,
        timeout=10,
    )

    if resposta.status_code == 429:
        retry = int(resposta.headers.get("Retry-After", 5))
        print(f"  Rate limit atingido. Aguardando {retry}s...")
        time.sleep(retry)
        return buscar_musicas(token, query, limite)

    if resposta.status_code != 200:
        print(f"  ⚠ Erro na busca '{query}': {resposta.status_code}")
        return []

    itens = resposta.json().get("tracks", {}).get("items", [])

    musicas = []
    for item in itens:
        musicas.append({
            "titulo":      item["name"],
            "artista":     item["artists"][0]["name"] if item["artists"] else "Desconhecido",
            "album":       item["album"]["name"],
            "ano":         int(item["album"]["release_date"][:4]) if item["album"].get("release_date") else None,
            "duracao_seg": item["duration_ms"] // 1000,
            "url_preview": item.get("external_urls", {}).get("spotify"),
            "spotify_id":  item["id"],
        })

    return musicas


def validar_musica(musica: dict) -> bool:
    """Valida se os campos obrigatórios estão presentes e corretos."""
    if not musica.get("titulo") or not musica.get("artista"):
        return False
    if musica.get("ano") and not (1900 <= musica["ano"] <= 2100):
        return False
    if musica.get("duracao_seg") and musica["duracao_seg"] <= 0:
        return False
    return True




def salvar_no_banco(musicas: list[dict], genero_nome: str, conn: sqlite3.Connection) -> tuple[int, int]:
    """
    Salva lista de músicas no banco SQLite.
    Cria o artista se ainda não existir.
    Retorna (salvas, ignoradas).
    """
    cur = conn.cursor()

    # Busca o ID do gênero
    cur.execute("SELECT id FROM generos WHERE nome = ?", (genero_nome,))
    row = cur.fetchone()
    if not row:
        print(f"  ⚠ Gênero '{genero_nome}' não encontrado no banco. Pulando.")
        return 0, len(musicas)

    genero_id = row[0]
    salvas = 0
    ignoradas = 0

    for m in musicas:
        if not validar_musica(m):
            ignoradas += 1
            continue

        cur.execute(
            "INSERT OR IGNORE INTO artistas (nome, genero_id) VALUES (?, ?)",
            (m["artista"], genero_id),
        )
        cur.execute("SELECT id FROM artistas WHERE nome = ?", (m["artista"],))
        artista_id = cur.fetchone()[0]

        cur.execute(
            "SELECT id FROM musicas WHERE titulo = ? AND artista_id = ?",
            (m["titulo"], artista_id),
        )
        if cur.fetchone():
            ignoradas += 1
            continue

        cur.execute(
            """INSERT INTO musicas (titulo, artista_id, genero_id, album, ano, duracao_seg, url_preview)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (m["titulo"], artista_id, genero_id, m["album"], m["ano"], m["duracao_seg"], m["url_preview"]),
        )
        salvas += 1

    conn.commit()
    return salvas, ignoradas


def importar_tudo():
    """
    Função principal: autentica, busca e importa músicas de todos os gêneros.
    """
    print("=" * 50)
    print("  Wavee — Importação via Spotify API")
    print("=" * 50)

    token = obter_token()
    conn  = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    total_salvas   = 0
    total_ignoradas = 0

    for genero, termos in GENEROS_BUSCA.items():
        print(f"\n🎵 Importando: {genero}")
        musicas_genero = []

        for termo in termos:
            print(f"  → Buscando: '{termo}'")
            resultado = buscar_musicas(token, termo, limite=LIMITE_POR_GENERO // len(termos) + 1)
            musicas_genero.extend(resultado)
            time.sleep(0.3)  # respeita rate limit

        # Remove duplicatas pelo spotify_id dentro do mesmo gênero
        vistos = set()
        unicas = []
        for m in musicas_genero:
            if m["spotify_id"] not in vistos:
                vistos.add(m["spotify_id"])
                unicas.append(m)

        salvas, ignoradas = salvar_no_banco(unicas[:LIMITE_POR_GENERO], genero, conn)
        total_salvas    += salvas
        total_ignoradas += ignoradas
        print(f"  ✓ {salvas} salvas | {ignoradas} ignoradas")

    conn.close()

    print("\n" + "=" * 50)
    print(f"  Importação concluída!")
    print(f"  Total salvas:   {total_salvas}")
    print(f"  Total ignoradas: {total_ignoradas}")
    print("=" * 50)


def validar_banco():
    """Exibe um relatório do estado atual do banco após a importação."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    print("Relatório de integridade do banco:")
    print("-" * 40)

    cur.execute("SELECT COUNT(*) FROM generos")
    print(f"  Gêneros:         {cur.fetchone()[0]}")

    cur.execute("SELECT COUNT(*) FROM artistas")
    print(f"  Artistas:        {cur.fetchone()[0]}")

    cur.execute("SELECT COUNT(*) FROM musicas")
    print(f"  Músicas:         {cur.fetchone()[0]}")

    print("\n  Músicas por gênero:")
    cur.execute("""
        SELECT g.nome, COUNT(m.id) as total
        FROM generos g
        LEFT JOIN musicas m ON m.genero_id = g.id
        GROUP BY g.nome ORDER BY total DESC
    """)
    for row in cur.fetchall():
        print(f"    {row['nome']:<15} {row['total']} músicas")

    cur.execute("SELECT COUNT(*) FROM musicas WHERE artista_id IS NULL")
    orfas = cur.fetchone()[0]
    if orfas:
        print(f"\n  ⚠ {orfas} música(s) sem artista vinculado!")
    else:
        print("\n  ✓ Todas as músicas têm artista vinculado.")

    conn.close()


if __name__ == "__main__":
    importar_tudo()
    validar_banco()
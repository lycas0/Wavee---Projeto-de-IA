from src.repositories.historico_repositorio import WaveeDB
from src.agent.cerebro_agente import CerebroAgente


class Agente:
    """
    Agente inteligente do Wavee (modelo PEAS).

    - Performance: acerto da classificação + feedback positivo do usuário
    - Environment: texto de entrada do usuário + banco de dados (generos,
      palavras-chave, associacoes aprendidas, historico)
    - Sensors: leitura do texto digitado e do histórico/associações no banco
    - Actuators: recomendação de músicas, exibição do gênero detectado e
      registro de interações/feedback no banco
    """

    def __init__(self, db_path: str = None):
        self.db = WaveeDB(db_path) if db_path else WaveeDB()
        self.cerebro = CerebroAgente(self.db)

    # --- Sensor: percebe o ambiente (entrada do usuário) ---
    def perceber(self, texto_usuario: str) -> str:
        return texto_usuario.strip()

    # --- Atuador: age sobre o ambiente (recomendação) ---
    def agir(self, texto_usuario: str, limite: int = 5):
        entrada = self.perceber(texto_usuario)

        genero, probabilidades, musicas = self.cerebro.recomendar(entrada, limite=limite)

        genero_row = self.db.genero_por_nome(genero)
        genero_id = genero_row["id"] if genero_row else None

        # registra a interação (sem música/clique específico ainda)
        self.db.registrar_interacao(
            entrada_texto=entrada,
            genero_id=genero_id,
            musica_id=None,
            clicou=False,
        )

        return {
            "genero": genero,
            "probabilidades": probabilidades,
            "musicas": musicas,
        }

    # ---Atuador: registra feedback do usuário sobre uma música ---
    def registrar_feedback(self, entrada_texto: str, genero_nome: str, musica_id: int, gostou: bool):
        genero_row = self.db.genero_por_nome(genero_nome)
        genero_id = genero_row["id"] if genero_row else None
        feedback = 1 if gostou else -1

        self.db.registrar_interacao(
            entrada_texto=entrada_texto,
            genero_id=genero_id,
            musica_id=musica_id,
            clicou=True,
            feedback=feedback,
        )

        # reforça a associação termo-genero quando o feedback é positivo
        if gostou and genero_id is not None:
            for termo in entrada_texto.lower().split():
                self.db.registrar_associacao(termo, genero_id)

    def encerrar(self):
        self.db.fechar()
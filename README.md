# Wavee - Projeto de IA

**Disciplina:** Introdução à Inteligência Artificial  
**Semestre:** 2026.1  
**Semestre:** [Semestre]  
**Professor:** ANDRE LUIS FONSECA FAUSTINO  
**Turma:** [T03 / T04]
**Turma:** [T0X]

## Integrantes do Grupo

- Bianca Bezerra Pires (20240020515)
- Estelita Fernanda Andre de Brito (20230072296)
- Marcus Vinicius de Oliveira (20250024670)
- Pedro Lucas Barbosa Nascimento (20250043522)

## Descrição do Projeto

O Wavee é um agente inteligente probabilístico capaz de receber uma palavra, frase ou trecho textual fornecido pelo usuário e calcular a probabilidade de pertencimento dessa entrada a diferentes gêneros musicais. Com base nesse cálculo, o agente identifica o gênero com maior probabilidade e realiza recomendações de músicas relacionadas, buscando aproximar as sugestões dos interesses expressos pelo usuário.
O sistema utiliza técnicas de classificação probabilística para transformar informações textuais em conhecimento útil para o processo de recomendação, permitindo que o usuário descubra novas músicas e artistas a partir de descrições simples ou palavras-chave.

## Guia de Instalação e Execução

[Descreva os passos para instalacao e execucao do projeto. Inclua um passo-a-passo claro de como utilizar a proposta desenvolvida. Veja o exemplo abaixo.]
[Descreva os passos para instalação e execução do projeto. Inclua um passo a passo claro de como utilizar a proposta desenvolvida. Veja o exemplo abaixo.]

### 1. Instalação das Dependências

Certifique-se de ter o **Python 3.x** instalado. Clone o repositório e instale as bibliotecas listadas no `requirements.txt`:
@@ -40,7 +40,7 @@ Execute o comando abaixo no terminal para iniciar o servidor local:
streamlit run src/app.py

```

Se necessário, especifique a porta ou url de acesso, ex: http://localhost:8501
Se necessário, especifique a porta ou url de acesso, ex.: http://localhost:8501

## Estrutura dos Arquivos

wavee-project/
│
├── data/                  # Banco de dados local
│
├── src/                   # Código fonte do projeto
│   │
│   ├── models/            # Entidades puras (Música, Artista, Gênero)
│   │   ├── artista.py
│   │   ├── genero.py
│   │   └── musica.py
│   │
│   ├── repositories/      # Comunicação com o banco de dados
│   │   └── historico_repositorio.py
│   │
│   ├── services/          # Consumo de APIs externas
│   │   └── music_api_service.py
│   │
│   ├── agent/             # O CORAÇÃO DA IA
│   │   ├── agente.py       # Classe Agente (contém o modelo probabilístico)
│   │   └── cerebro_agente.py       # O algoritmo em si (ex: Naive Bayes, tabelas de probabilidade)
│   │
│   └── view/              # Interface Gráfica
│       └── app_window.py  # Telas, botões e campos de texto
│
├── main.py                # Arquivo principal que inicializa e amarra tudo
└── requirements.txt       # Bibliotecas necessárias

## Modelo PEAS do Agente

| Elemento     | Descrição |
|--------------|-----------|
| **Performance** | Acerto na classificação do gênero musical e qualidade das recomendações, medidos pelo feedback do usuário (positivo/negativo) registrado no histórico. |
| **Environment** | O texto fornecido pelo usuário e o banco de dados Wavee (gêneros, palavras-chave, artistas, músicas, associações aprendidas e histórico de interações). |
| **Actuators** | Exibição do gênero identificado, recomendação de músicas e registro de interações/feedback no banco de dados. |
| **Sensors** | Leitura e tokenização do texto digitado pelo usuário, além da leitura do histórico e das associações aprendidas no banco. |

### Algoritmo do Agente

1. O usuário fornece um texto (palavra, frase ou trecho).
2. A **Rede Bayesiana** (`rede_bayesiana.py`) calcula a probabilidade do texto pertencer a cada gênero, com base nas palavras-chave cadastradas e nas associações aprendidas com feedback anterior.
3. O **Cérebro do Agente** (`cerebro_agente.py`) escolhe o gênero mais provável e busca músicas correspondentes no banco.
4. A **Heurística** (`heuristica.py`) pode ser usada para ranquear músicas considerando também o histórico de cliques.
5. O **Agente** (`agente.py`) registra a interação no banco e, ao receber feedback do usuário, reforça as associações termo-gênero para aprendizado contínuo.
```

# Wavee - Projeto de Inteligência Artificial

**Disciplina:** Introdução à Inteligência Artificial
**Semestre:** 2026.1
**Professor:** André Luis Fonseca Faustino
**Turma:** T03

## Integrantes do Grupo

* Bianca Bezerra Pires (20240020515)
* Estelita Fernanda André de Brito (20230072296)
* Marcus Vinicius de Oliveira (20250024670)
* Pedro Lucas Barbosa Nascimento (20250043522)

## Descrição do Projeto

O Wavee é um agente inteligente híbrido que combina técnicas probabilísticas e heurísticas para recomendar músicas a partir de palavras, frases ou trechos textuais informados pelo usuário.

O sistema utiliza um classificador probabilístico baseado no algoritmo **Naive Bayes** para estimar o gênero musical mais compatível com a entrada textual fornecida. Em seguida, uma estratégia de **Busca Gulosa** é aplicada para selecionar e ordenar as músicas mais relevantes dentre as candidatas disponíveis.

A avaliação das músicas é realizada por uma função heurística que combina a probabilidade calculada pelo classificador com o histórico de interações registradas pelos usuários. Dessa forma, o sistema adapta suas recomendações ao longo do tempo, priorizando músicas que apresentaram maior relevância em buscas anteriores.

---

## Guia de Instalação e Execução

### 1. Instalação das Dependências

Certifique-se de possuir o Python 3.x instalado em sua máquina.

Clone o repositório e instale as dependências:

```bash
pip install -r requirements.txt
```

### 2. Execução do Projeto

Para iniciar a aplicação:

```bash
python main.py
```

---

## Estrutura do Projeto

```text
Wavee---Projeto-de-IA/
│
├── assets/
│   └── logo_wavee.png          # Logotipo da aplicação
│
├── data/
│   ├── init_db.py             # Script de criação e inicialização do banco
│   └── wavee.db               # Banco de dados SQLite
│
├── src/
│   ├── agent/                 # Componentes de Inteligência Artificial
│   ├── models/                # Entidades do sistema
│   ├── repositories/          # Acesso e persistência de dados
│   └── view/                  # Interface gráfica da aplicação
│
├── main.py                    # Ponto de entrada do sistema
├── requirements.txt           # Dependências do projeto
└── README.md                  # Documentação do projeto
```

---

## Modelo PEAS

| Elemento        | Descrição                                                                                             |
| --------------- | ----------------------------------------------------------------------------------------------------- |
| **Performance** | Maximizar a relevância das recomendações musicais e a precisão da classificação de gênero.            |
| **Environment** | Interface gráfica Tkinter, banco de dados SQLite e conjunto de músicas cadastradas.                   |
| **Actuators**   | Exibição das recomendações, atualização dos componentes visuais e registro das interações do usuário. |
| **Sensors**     | Captura da entrada textual e consulta aos dados armazenados no banco.                                 |

---

## Fluxo de Funcionamento do Agente

### 1. Percepção

O usuário fornece uma palavra, frase ou trecho textual através da interface gráfica.

### 2. Classificação Probabilística

A Rede Bayesiana baseada em Naive Bayes processa os termos da entrada e calcula a probabilidade de associação com cada gênero musical cadastrado.

### 3. Seleção de Candidatas

O sistema identifica o gênero mais provável e recupera do banco de dados as músicas pertencentes a esse gênero.

### 4. Busca Gulosa

As músicas candidatas são avaliadas por uma função heurística. A Busca Gulosa seleciona primeiro as músicas que apresentam maior valor heurístico, priorizando aquelas consideradas mais relevantes para o contexto da busca.

A função heurística é definida como:

h(n) = (α × PesoHistórico) + (β × ProbabilidadeGênero)

onde:

* **PesoHistórico** representa a frequência de interações anteriores dos usuários com a música;
* **ProbabilidadeGênero** corresponde ao valor calculado pelo classificador Naive Bayes;
* **α** e **β** são coeficientes de ponderação.

### 5. Ação

O agente apresenta ao usuário as músicas recomendadas e exibe o gênero identificado.

### 6. Atualização do Histórico

Quando o usuário seleciona uma música recomendada, a interação é registrada no banco de dados. Esse histórico passa a influenciar futuras avaliações heurísticas, permitindo que o sistema ajuste gradualmente suas recomendações.


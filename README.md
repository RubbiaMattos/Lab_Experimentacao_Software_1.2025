# 📊 Laboratórios de Experimentação de Software

Bem-vindo(a) ao repositório dos **Laboratórios de Experimentação de Software** da disciplina de **Engenharia de Software** (PUC Minas). Aqui você encontrará cinco experimentos práticos que abordam desde análise de repositórios GitHub até criação de dashboards e comparação de APIs.

---

## 📑 Sumário

1. [Visão Geral](#-visão-geral)
2. [Pré-requisitos](#-pré-requisitos)
3. [Laboratórios](#-laboratórios)
4. [Como Executar](#-como-executar)
5. [Saídas Esperadas](#-saídas-esperadas)
6. [Tecnologias e Ferramentas](#-tecnologias-e-ferramentas)
7. [Estrutura do Repositório](#-estrutura-do-repositório)
8. [Equipe e Contato](#-equipe-e-contato)

---

## 🔍 Visão Geral

Este repositório centraliza todos os laboratórios realizados na disciplina de **Laboratório de Experimentação de Software**, com foco em:

* **Design Experimental:** definição de hipóteses, variáveis e tratamentos.
* **Automação:** coleta e análise de dados via scripts em Python e Java.
* **Análise Estatística:** uso de correlações, testes de hipóteses e visualizações.
* **Visualização:** criação de dashboards interativos e gráficos informativos.

Cada laboratório documenta seu objetivo, passos de execução, saídas esperadas e resultados.

---

## ⚙️ Pré-requisitos

Antes de começar, certifique-se de ter instalado:

* **Python 3.8+** (com `pip`)
* **Java Runtime Environment (JRE) 8+** (para executar `ck.jar` no Lab 2)
* **Git** (para clonar o repositório)
* **Ferramenta de BI** (Power BI Desktop, Tableau ou Google Data Studio) – necessária para o Lab 4
* **Variável de ambiente** `GITHUB_TOKEN` configurada para acessar a GitHub API (Lab 1, 2, 3 e 5)

---

## 📌 Laboratórios

| Lab | Tema                                                   | Diretório         |
| :-: | ------------------------------------------------------ | ----------------- |
|  1  | Características de Repositórios Populares (GitHub API) | `Lab1_RepoPop`    |
|  2  | Qualidade de Sistemas Java (Métricas CK)               | `Lab2_QualiJava`  |
|  3  | Atividade de Code Review no GitHub                     | `Lab3_CodeReview` |
|  4  | Visualização de Dados com BI (CAGED)                   | `Lab4_BI`         |
|  5  | GraphQL vs REST (GitHub API)                           | `Lab5_GraphXRest` |

Cada pasta contém:

* **Enunciado** (`.pdf`)
* **README** específico com instruções detalhadas
* **Scripts** para coleta, análise e geração de relatórios
* **Pastas** de resultados: CSVs, gráficos, dashboards e artefatos finais

---

## 🚀 Como Executar

Para qualquer laboratório, siga estes passos:

1. **Clone o repositório**

   ```bash
   git clone https://github.com/RubbiaMattos/Lab_Experimentacao_Software_1.2025.git
   ```

2. **Acesse o diretório do laboratório**

   ```bash
   cd LabX_NomeDoLab
   ```

3. **Instale as dependências**

   Execute o comando abaixo para instalar todas as bibliotecas Python necessárias para todos os laboratórios:

   ```bash
   pip install requests pandas matplotlib seaborn python-dotenv scipy statsmodels GitPython jupyter PyGithub python-dateutil tqdm pyodbc tabulate
   ```

4. **Configure o token GitHub**

   * Edite o arquivo `env.config` (na raiz do repositório) e defina:

     ```ini
     GITHUB_TOKEN=seu_token_aqui
     ```
   * O script `config_token.py` carregará essa variável para os demais pipelines.

5. **Execute o pipeline principal**

   ```bash
   python main.py --step all
   ```

   ou siga as instruções passo a passo no README de cada laboratório.

---

## 📂 Saídas Esperadas

| Lab | Principais Arquivos de Saída                                           |
| :-: | ---------------------------------------------------------------------- |
|  1  | CSV de métricas (`*.csv`), gráficos (`.png`), relatório (`.pdf/.pptx`) |
|  2  | `resultados_totais.csv`, gráficos CK (`.png`), relatório final         |
|  3  | `selected_repos.csv`, `collected_prs.csv`, `report.md`, `Figuras/`     |
|  4  | Arquivo Power BI (`.pbix`), exportações PDF, relatório Word/DOCX       |
|  5  | `experiment_results.csv`, `experiment_summary.csv`, `Gráficos/`, JSON  |

---

## 🛠️ Tecnologias e Ferramentas

* **Linguagens:** Python (3.8+), Java (Lab 2)
* **API:** GitHub REST & GraphQL
* **BI:** Power BI Desktop, Tableau, Google Data Studio
* **Análise Java:** `ck.jar` para métricas de código

## 📚 Bibliotecas Python Utilizadas

A seguir, todas as bibliotecas Python necessárias, agrupadas por laboratório:

**Em todos os laboratórios:**

* `requests`
* `pandas`
* `matplotlib`
* `seaborn`
* `python-dotenv`
* `scipy`
* `statsmodels`
* `GitPython`
* `jupyter`

**Lab 1 – `Lab1_RepoPop`:**

* `PyGithub` (para interagir com GraphQL/REST)
* `tqdm` (barra de progresso opcional)

**Lab 2 – `Lab2_QualiJava`:**

* nenhuma biblioteca adicional em Python (uso de `subprocess` para executar `ck.jar`)

**Lab 3 – `Lab3_CodeReview`:**

* `PyGithub`
* `python-dateutil` (para manipulação avançada de datas)

**Lab 4 – `Lab4_BI`:**

* `pyodbc` ou `pandas` (para preparar dados de entrada)
* `tabulate` (para exportar tabelas, opcional)

**Lab 5 – `Lab5_GraphXRest`:**

* nenhuma biblioteca adicional além das comuns (uso de `requests` para REST/GraphQL)

---

## 🗂️ Estrutura Geral do Repositório

```
Lab_Experimentacao_Software_1.2025
├── Lab1_RepoPop/                       # Lab 1: Repositórios Populares (GraphQL/REST)
├── Lab2_QualiJava/                     # Lab 2: Métricas CK em Java
├── Lab3_CodeReview/                    # Lab 3: Atividade de Code Review
├── Lab4_BI/                            # Lab 4: Dashboards BI (CAGED)
├── Lab5_GraphXRest/                    # Lab 5: GraphQL vs REST
├── 📄 README.md                        # Visão geral (este arquivo)
├── 📄 config_token.py                  # Carrega token GitHub (.env) para os scripts
├── 📄 config_token_rotator.py          # Gerencia rotação automática de tokens
└── 📄 env.config                       # Armazena variáveis de ambiente (GITHUB_TOKEN)
```

---

## 👥 Equipe e Contato

* **Nataniel Geraldo Mendes Peixoto**
* **Nelson de Campos Nolasco**
* **Rubia Coelho de Matos**

---

*Disciplina: Laboratório de Experimentação de Software — PUC Minas*


# 🧪 Laboratório 03 — Caracterizando a Atividade de Code Review no GitHub

## 🎯 Objetivo

Analisar a atividade de **code review** em repositórios populares do GitHub, investigando variáveis que influenciam o merge de Pull Requests (PRs) e o número de revisões realizadas.

---

## 🗂️ Etapas do Projeto

1. **Seleção de Repositórios**  
   - Coletar os 200 repositórios mais populares (stars > 1000) com ao menos 100 PRs.  
2. **Coleta de PRs**  
   - Extrair PRs com status MERGED ou CLOSED, com pelo menos uma revisão e tempo de análise ≥ 1 hora.  
3. **Preparação do Dataset**  
   - Consolidar métricas: número de arquivos alterados, linhas adicionadas/removidas, tempo de análise, tamanho da descrição, número de comentários e participantes únicos.  
4. **Análise Estatística**  
   - Cálculo de correlações de Spearman para cada RQ.  
   - Geração de boxplots, histogramas e scatter-plots para visualização.  
5. **Documentação e Relatórios**  
   - Gerar relatório em Markdown/PDF e apresentação em PPTX.

---

## 🛠️ Como Executar

### 🔐 Configuração

1. Crie o arquivo `.env` na raiz do projeto:
   ```ini
   GITHUB_TOKEN=seu_token_gh_aqui
````

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

### ▶️ Pipeline Completo

No terminal:

```bash
python main.py --step all
```

> Ou por etapas:
>
> ```bash
> python main.py --step collect_repos   # Seleção de repositórios
> python main.py --step collect_prs     # Coleta e filtragem de PRs
> python main.py --step analyze        # Gera análises e gráficos
> ```

---

### 📂 Saídas esperadas

* `selected_repos.csv`: arquivo CSV com os repositórios selecionados
* `collected_prs.csv`: arquivo CSV com os Pull Requests extraídos e filtrados
* `report.md`: relatório em Markdown contendo análises e respostas às RQs
* `Análise Características CodeReview GitHub.pdf`: versão em PDF do relatório
* `Análise Características CodeReview GitHub.pptx`: apresentação em PowerPoint
* Diretório `Figuras/`: todos os gráficos gerados no formato PNG

---

## 🔎 Questões de Pesquisa (RQs)

| RQ   | Pergunta                                                                                             |
| ---- | ---------------------------------------------------------------------------------------------------- |
| RQ01 | Qual a relação entre o **tamanho** dos PRs e o **feedback final** (merged vs. closed)?               |
| RQ02 | Qual a relação entre o **tempo de análise** dos PRs e o **feedback final**?                         |
| RQ03 | Qual a relação entre o **tamanho da descrição** dos PRs e o **feedback final**?                     |
| RQ04 | Qual a relação entre as **interações** nos PRs e o **feedback final**?                              |
| RQ05 | Qual a relação entre o **tamanho** dos PRs e o **número de revisões** efetuadas?                    |
| RQ06 | Qual a relação entre o **tempo de análise** dos PRs e o **número de revisões** efetuadas?           |
| RQ07 | Qual a relação entre o **tamanho da descrição** dos PRs e o **número de revisões** efetuadas?       |
| RQ08 | Qual a relação entre as **interações** nos PRs e o **número de revisões** efetuadas?                |

---

## 📈 Métricas Utilizadas

| Categoria      | Métrica                                                                                        |
| -------------- | ---------------------------------------------------------------------------------------------- |
| **Tamanho**    | • Número de arquivos alterados<br>• Linhas adicionadas<br>• Linhas removidas                   |
| **Tempo**      | • Horas entre criação e fechamento do PR                                                       |
| **Descrição**  | • Número de caracteres na descrição do PR                                                      |
| **Interações** | • Total de comentários<br>• Número de revisões (reviews)<br>• Participantes únicos (revisores) |
| **Resultado**  | • Status final do PR (merged vs. closed)                                                       |

---

## 👥 Equipe

* Nataniel Geraldo Mendes Peixoto
* Nelson de Campos Nolasco
* Rubia Coelho de Matos

---

## 📂 Estrutura do Projeto

```
Lab3_CodeRevGithub/
├── 📄 main.py                              # Orquestra o pipeline
├── 📄 collect_repos.py                     # Seleção de repositórios GitHub
├── 📄 collect_prs.py                       # Coleta e filtragem de PRs
├── 📄 analyze_data.py                      # Estatísticas e visualizações
├── 📄 utils.py                             # Funções auxiliares
├── 📄 LABORATÓRIO_03.pdf                   # Enunciado do laboratório
├── 📄 README_Lab3.md                       # Documentação do projeto

├── 📂 Relatórios/                          # Relatórios e artefatos finais
│   ├── 📄 report.md                        # Relatório em Markdown
│   ├── 📄 Análise Características CodeReview GitHub.pdf
│   ├── 📄 Análise Características CodeReview GitHub.pptx
│   └── 📂 Figuras/                         # Gráficos gerados (PNG)
│       ├── rq01_additions_boxplot.png
│       ├── rq01_correlation.png
│       ├── rq01_deletions_boxplot.png
│       ├── rq01_files_changed_boxplot.png
│       ├── rq02_time_histogram.png
│       ├── rq02_time_boxplot.png
│       ├── rq03_description_bars.png
│       ├── rq03_description_boxplot.png
│       ├── rq04_comments_boxplot.png
│       ├── rq04_participant_count_boxplot.png
│       ├── rq04_correlation.png
│       ├── rq05_files_changed_scatter.png
│       ├── rq05_additions_scatter.png
│       ├── rq05_deletions_scatter.png
│       ├── rq05_correlation.png
│       ├── rq06_time_scatter.png
│       ├── rq06_time_bins.png
│       ├── rq07_description_scatter.png
│       ├── rq07_desc_bins.png
│       ├── rq08_comments_scatter.png
│       ├── rq08_participant_count_scatter.png
│       ├── rq08_review_comments_scatter.png
│       └── rq08_correlation.png
```

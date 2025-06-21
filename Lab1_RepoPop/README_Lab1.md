# 🧪 Laboratório 01 — Análise de Repositórios Populares no GitHub

## 🎯 Objetivo

Investigar características de sistemas populares open-source, com base nos 1.000 repositórios mais estrelados no GitHub. As análises envolvem:

* Idade (maturidade)
* Contribuição externa (pull requests aceitas)
* Frequência de lançamentos (releases)
* Frequência de atualização (último push)
* Linguagem de programação mais comum
* Percentual de issues fechadas

---

## 🗂️ Etapas do Projeto

1. **Coleta de Repositórios com GraphQL API**

   * Paginação para capturar 1000 repositórios
   * Dados exportados para `.csv`

2. **Análise dos Dados Coletados**

   * Cálculo de medianas por métrica
   * Contagens por categoria (ex: linguagens)
   * Visualização de dados com gráficos

3. **Relatório Final**

   * Resposta às RQs
   * Hipóteses e discussão dos resultados
   * Geração de documentos e gráficos

---

## 🛠️ Como Executar

### 🔐 Configuração do Token

Crie o arquivo `env.config` no caminho:

```
2025-1 - 2º, 6º PERÍODO\LABORATÓRIO DE EXPERIMENTAÇÃO DE SOFTWARE\Lab_Experimentacao_Software_1.2025\env.config
```

Com o seguinte conteúdo:

```
GITHUB_TOKEN=seu_token_aqui
```

Para gerar o token, acesse: [GitHub Developer Settings](https://github.com/settings/tokens)
→ Clique em **Generate new token (classic)** e selecione o escopo `repo`.

> ⚠️ **Importante:** Nunca compartilhe seu token publicamente.

---

### ▶️ Etapas de Execução

1. **Instale as dependências:**

```bash
py -3.12 -m pip install pandas requests matplotlib seaborn python-dotenv
```

2. **Execute o script principal:**

```bash
python Lab1_RepoPop/Lab01S03/RepoPop1000Final.py
```
--- 

### 📂 Saídas esperadas

* `github_analysis.csv`: dados coletados e analisados&#x20;
* Gráficos `.png` com visualizações por métrica&#x20;
* Relatório final em `.docx`, `.pdf` e `.pptx` na pasta `Relatórios`&#x20;

---
## ❓ Questões de Pesquisa (RQs)

| RQ  | Pergunta                                                                  | Métrica                                    |
| --- | ------------------------------------------------------------------------- | ------------------------------------------ |
| RQ1 | Sistemas populares são maduros/antigos?                                   | Idade do repositório                       |
| RQ2 | Sistemas populares recebem muita contribuição externa?                    | Total de pull requests aceitas             |
| RQ3 | Sistemas populares lançam releases com frequência?                        | Total de releases                          |
| RQ4 | Sistemas populares são atualizados com frequência?                        | Tempo desde a última atualização (em dias) |
| RQ5 | Sistemas populares são escritos nas linguagens mais populares?            | Linguagem principal do repositório         |
| RQ6 | Sistemas populares possuem um alto percentual de issues fechadas?         | Ratio: issues fechadas / total de issues   |
| RQ7 | Linguagens populares afetam contribuição, releases e atualização? (bônus) | Análise por linguagem das RQs 2, 3 e 4     |

---

## 📈 Métricas Utilizadas

| Categoria            | Métricas                                          |
| -------------------- | ------------------------------------------------- |
| Maturidade           | Idade do repositório                              |
| Colaboração Externa  | Total de pull requests aceitas                    |
| Atividade            | Total de releases, tempo desde última atualização |
| Popularidade         | Número de estrelas (filtro inicial)               |
| Linguagem            | Linguagem primária                                |
| Qualidade Processual | Percentual de issues fechadas                     |

---

## 👥 Equipe

* **Nataniel Geraldo Mendes Peixoto**
* **Nelson de Campos Nolasco**
* **Rubia Coelho de Matos**

---

## 📁 Estrutura do Projeto

```
📦 Lab1_RepoPop/
├── 📄 RepoPop1000Final.py                # Script principal de coleta e análise
├── 📄 LABORATÓRIO_01.pdf                 # Enunciado do laboratório
├── 📄 README_Lab1.md                     # Documentação do projeto
│
├── 📂 Relatórios/
│   ├── 📄 Análise de Repositórios Populares no GitHub.docx
│   ├── 📄 Análise de Repositórios Populares no GitHub.pdf
│   ├── 📄 Analise Repositorios Populares.pptx
│   ├── 📊 dias_desde_ultima_atualizacao.png
│   ├── 📊 idade_repositorios.png
│   ├── 📊 metricas_por_linguagem.png
│   ├── 📊 percentual_issues_fechadas.png
│   ├── 📊 qtd_PRs_aceitos.png
│   ├── 📊 qtd_releases.png
│   ├── 📊 top_languages.png
│
│   └── 📂 Figuras/
│       ├── dias_desde_ultima_atualizacao.png
│       ├── idade_repositorios.png
│       ├── metricas_por_linguagem.png
│       ├── percentual_issues_fechadas.png
│       ├── qtd_PRs_aceitos.png
│       ├── qtd_releases.png
│       └── top_languages.png
```
# 🧪 Laboratório 02 — Análise de Qualidade em Repositórios Java

## 🎯 Objetivo

Investigar a relação entre métricas de qualidade de código-fonte (CBO, DIT, LCOM) e características de desenvolvimento de repositórios populares em **Java**, como:

* Popularidade (estrelas)
* Maturidade (idade)
* Atividade (releases)
* Tamanho (LOC e comentários)

---

## 🗂️ Etapas do Projeto

1. **Coleta dos Repositórios Java via API do GitHub**

   * Filtro por licença open-source
   * Ordenação por número de estrelas

2. **Clonagem Automatizada dos Repositórios**

   * Verificação de integridade (`.git`)
   * Tolerância a falhas e re-clone quando necessário

3. **Extração de Métricas CK**

   * Utilização do `ck.jar` para gerar métricas de qualidade: CBO, DIT, LCOM, LOC, Comentários

4. **Análise Estatística e Visualizações**

   * Estatísticas descritivas
   * Histogramas, boxplots
   * Correlações (Pearson e Spearman)
   * Regressão linear múltipla

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
py -3.12 -m pip install pandas requests matplotlib seaborn python-dotenv statsmodels scipy tabulate tqdm psutil
```

2. **Execute o pipeline completo:**

```bash
python main.py --step all
```

3. **Ou execute por etapas:**

```bash
python main.py --step buscar      # Buscar repositórios Java via API
python main.py --step clone       # Clonar os repositórios
python main.py --step coletar     # Executar ck.jar e extrair métricas
python main.py --step analisar    # Analisar métricas e gerar gráficos
```

> Também é possível executar os scripts individualmente:
> `coleta_repositorios.py`, `automacao_clone.py`, `coletar_dados.py`, `analisar_dados.py`

---

### 📂 Saídas esperadas

* `data/resultados_totais.csv`: arquivo com métricas extraídas (CBO, DIT, LCOM etc.)
* Diretório `Repos/`: repositórios Java clonados
* Diretório `Relatórios/`:

  * Gráficos `.png` gerados pela análise
  * Relatórios em `.docx`, `.pdf`, `.pptx`
  * Logs de execução `.log`

---

## ❓ Questões de Pesquisa (RQs)

| RQ  | Pergunta                                                             | Hipótese                                   |
| --- | -------------------------------------------------------------------- | ------------------------------------------ |
| RQ1 | Qual a relação entre a **popularidade** e atributos de qualidade?    | Populares têm melhor qualidade             |
| RQ2 | Qual a relação entre a **maturidade** e qualidade?                   | Repositórios antigos têm melhor qualidade  |
| RQ3 | Repositórios com mais **atividade** (releases) têm melhor qualidade? | Atividade pode afetar coesão e acoplamento |
| RQ4 | Repositórios maiores (em **LOC**) têm pior qualidade?                | Tamanho pode aumentar complexidade         |

---

## 📈 Métricas Utilizadas

| Categoria    | Métricas                     |
| ------------ | ---------------------------- |
| Qualidade    | CBO, DIT, LCOM               |
| Tamanho      | LOC, Comentários             |
| Popularidade | Estrelas (Stars)             |
| Atividade    | Número de releases           |
| Maturidade   | Tempo desde a criação (anos) |

---

## 👥 Equipe

* **Nataniel Geraldo Mendes Peixoto**
* **Nelson de Campos Nolasco**
* **Rubia Coelho de Matos**

---

## 📁 Estrutura do Projeto

```
📦 Lab2_QualiJava/
├── 📄 main.py                         # Gerencia a execução por etapas
├── 📄 LABORATÓRIO_02.pdf             # Enunciado do laboratório
├── 📄 README_Lab2.md                 # Documentação do projeto
│
├── 🐍 coleta_repositorios.py         # Coleta repositórios Java via GitHub API
├── 🐍 automacao_clone.py            # Clona repositórios encontrados
├── 🐍 coletar_dados.py              # Executa CK (ck.jar) e extrai métricas
├── 🐍 analisar_dados.py             # Gera gráficos e análises estatísticas
├── 📄 ck.jar                         # Ferramenta para extração de métricas CK
├── 📄 env.config                     # Token pessoal do GitHub (não versionar)
│
├── 📂 data/
│   └── resultados_totais.csv        # Métricas extraídas com o CK
│
├── 📂 Repos/
│   └── ... (repositórios Java clonados)
│
├── 📂 Relatórios/
│   ├── 📄 Análise de Repositórios Populares Java GitHub.docx
│   ├── 📄 Análise de Repositórios Populares Java GitHub.pdf
│   ├── 📄 Analise Características Qualidade Repositórios Java.pptx
│   ├── 📄 analisar_dados_log.log
│   ├── 📄 clone_repositorios_log.log
│   ├── 📄 coleta_repositorios_log.log
│   ├── 📄 coletar_dados_log.log
│
│   ├── 📊 boxplot_LOC.png
│   ├── 📊 histograma_CBO.png
│   ├── 📊 histograma_Comments.png
│   ├── 📊 histograma_DIT.png
│   ├── 📊 histograma_LCOM.png
│   ├── 📊 histograma_LOC.png
│   ├── 📊 histograma_Maturity.png
│   ├── 📊 histograma_Release.png
│   ├── 📊 histograma_Stars.png
│
│   ├── 📊 loc_qualidade_CBO.png
│   ├── 📊 loc_qualidade_DIT.png
│   ├── 📊 loc_qualidade_LCOM.png
│
│   ├── 📊 maturidade_qualidade_CBO.png
│   ├── 📊 maturidade_qualidade_DIT.png
│   ├── 📊 maturidade_qualidade_LCOM.png
│
│   ├── 📊 popularidade_qualidade_CBO.png
│   ├── 📊 popularidade_qualidade_DIT.png
│   ├── 📊 popularidade_qualidade_LCOM.png
│
│   ├── 📊 release_qualidade_CBO.png
│   ├── 📊 release_qualidade_DIT.png
│   └── 📊 release_qualidade_LCOM.png
```

---
# 🧪 Laboratório 04 — Visualização de Dados com Business Intelligence (BI)

## 🎯 Objetivo

Utilizar ferramentas de **Business Intelligence (BI)** — como Power BI, Tableau ou Google Data Studio — para explorar dados do mercado de trabalho formal no Brasil com foco em **tecnologia da informação (TI)**, baseando-se no dataset **CAGED (Cadastro Geral de Empregados e Desempregados)**.

A proposta visa analisar e apresentar de forma visual as seguintes questões:

* Qual a distribuição salarial por estado para ocupações em TI?
* Existe correlação entre idade e remuneração?
* Há disparidades salariais entre gêneros?

---

## 🗂️ Etapas do Projeto

1. **Coleta e Caracterização do Dataset (CAGED)**

   * Filtros aplicados para área de tecnologia
   * Identificação das colunas relevantes (salário, idade, UF, sexo, ocupação)

2. **Exploração e Preparação dos Dados**

   * Importação para o Power BI
   * Limpeza e modelagem dos dados

3. **Criação do Dashboard**

   * Visualizações interativas para responder às questões de pesquisa
   * Inclusão de filtros por UF, faixa etária e gênero

4. **Análise e Geração de Relatórios**

   * Painel final exportado em PDF
   * Relatório com interpretações e insights

---

## 🤖 Como Executar

### 💻 Ferramenta Utilizada

* **Microsoft Power BI**

### 📦 Arquivos Relevantes

* `PUCMG - Laboratório 04.pbix` → Arquivo com o dashboard
* `CAGED.pdf` → Descrição oficial da base de dados
* `Relatorio CAGED - Tecnologia.docx` → Relatório analítico com interpretações
* `Questões de Pesquisa - RQs.pdf` → Documento com as perguntas principais
* `Apresentação - Explorando o Dataset CAGED_Reduzido.pdf` → Slides usados em sala

### ▶️ Etapas

1. **Abrir o projeto no Power BI**

   ```bash
   Abrir o arquivo .pbix no Power BI Desktop
   ```

2. **Explorar as visualizações e aplicar filtros**

   * Use os slicers para refinar por estado, sexo ou faixa etária

3. **Exportar o dashboard**

   ```bash
   Arquivo → Exportar → PDF
   ```

4. **Consultar o relatório e apresentações**

   * Interprete os gráficos com base nas questões de pesquisa
   * Os arquivos PDF e DOCX explicam os achados principais

---

### 📂 Saídas Esperadas

* `PUCMG - Laboratório 04.pbix`
  Arquivo do dashboard desenvolvido no Power BI.
* PDF exportado do dashboard
  (por exemplo, via **Arquivo → Exportar → PDF** no Power BI; nome sugerido: `Dashboard_CAGED.pdf`).
* `Relatorio CAGED - Tecnologia.docx`
  Relatório analítico em Word com interpretações dos achados.
* `Apresentação - Explorando o Dataset CAGED_Reduzido.pdf`
  Slides em PDF usados em sala.
* `Apresentação - Explorando o Dataset CAGED.pptx`
  Arquivo de apresentação em PowerPoint.

---

## ❓ Questões de Pesquisa (RQs)

| RQ  | Pergunta                                                                                |
| --- | --------------------------------------------------------------------------------------- |
| RQ1 | Qual a média salarial dos profissionais de tecnologia nos diversos estados brasileiros? |
| RQ2 | Existe correlação entre a idade e a média salarial no setor de tecnologia?              |
| RQ3 | Há disparidades salariais entre homens e mulheres em cargos semelhantes?                |

---

## 📈 Métricas Utilizadas

| Métrica        | Descrição                                  |
| -------------- | ------------------------------------------ |
| Média Salarial | Salário médio por UF, sexo, idade          |
| Faixa Etária   | Agrupamento de idade (ex: 18–25, 26–35...) |
| Ocupação       | Filtros baseados em palavras-chave de TI   |
| Gênero         | Comparativo entre masculino e feminino     |
| UF             | Estado de registro do contrato de trabalho |

---

## 👥 Equipe

* **Nataniel Geraldo Mendes Peixoto**
* **Nelson de Campos Nolasco**
* **Rubia Coelho de Matos**

---

## 📁 Estrutura do Projeto

```
📦 Lab4_VizuDadosFerBI/
├── 📄 README_Lab4.md
├── 📄 LABORATÓRIO_04.pdf                     # Enunciado oficial do laboratório
├── 📄 Questões de Pesquisa - RQs.pdf         # Documento com RQs definidas
├── 📄 Relatorio CAGED - Tecnologia.docx      # Relatório descritivo do projeto
├── 📄 Apresentação - Explorando o Dataset CAGED_Reduzido.pdf
├── 📄 Apresentação - Explorando o Dataset CAGED.html
├── 📄 CAGED.pdf                              # Documento de apoio técnico
├── 📄 PUCMG - Laboratório 04.pbix            # Dashboard do projeto em Power BI
│
├── 📂 Dataset-CAGED-02_2025/                 # Conjunto de dados utilizado
│   ├── 📄 manual_caged_2019.pdf
│   ├── 📄 manual_treinamento_caged_rais.pdf
│   └── 📂 CAGEDMOV202502.7z/
│       └── 📄 CAGEDMOV202502.txt             # Arquivo de dados principal
```
---
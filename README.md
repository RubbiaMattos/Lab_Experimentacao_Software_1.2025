# 📊 Laboratórios de Experimentação de Software

Este repositório contém os **laboratórios de experimentação** realizados na disciplina **Laboratório de Experimentação de Software** do curso de **Engenharia de Software** da **PUC Minas**, com foco em boas práticas de desenvolvimento de software e tecnologias emergentes. Cada laboratório tem um conjunto específico de objetivos, análises e resultados esperados.

---

## 📌 **Laboratórios e Instruções em Cada Pasta**

Cada pasta de laboratório contém um **README** detalhado com as instruções específicas para execução do experimento. Abaixo, você encontrará uma visão geral do que cada pasta contém e o que você pode esperar em cada uma delas.

### 🔹 **[Laboratório 01 - Características de Repositórios Populares](Lab1_RepoPop)**

**Objetivo:** Analisar as características dos repositórios mais populares do GitHub, como maturidade, atividade e contribuições externas.

**Instruções na pasta:**
- Como configurar o **token de autenticação** do GitHub.
- Passos para executar o script `RepoPop100.py`, que coleta dados de repositórios populares utilizando **GraphQL**.
- Detalhes sobre os arquivos gerados, como gráficos e arquivos CSV com métricas (Pull Requests, Releases, etc.).
- Como visualizar os resultados utilizando ferramentas como Excel, Google Sheets ou Python.

---

### 🔹 **[Laboratório 02 - Qualidade de Sistemas Java](Lab2_QualiJava)**

**Objetivo:** Analisar a qualidade de código de repositórios Java open-source utilizando métricas como **acoplamento**, **coesão** e **complexidade**.

**Instruções na pasta:**
- Como configurar o **token do GitHub** para coletar dados dos repositórios.
- Passos para rodar os scripts de coleta de repositórios (`coleta_repositorios.py`) e análise de métricas com a ferramenta **CK** (`coletar_dados.py`).
- Instruções para instalar as dependências e como gerar os arquivos de saída contendo métricas de código (como `class.csv`, `method.csv`, etc.).
- Como analisar os dados coletados para correlacionar métricas de qualidade com popularidade, maturidade e atividade.

---

### 🔹 **[Laboratório 03 - Code Review no GitHub](Lab3_)**

**Objetivo:** Analisar a atividade de **code review** nos repositórios populares do GitHub e identificar fatores que influenciam a aceitação de Pull Requests (PRs).

**Instruções na pasta:**
- Como configurar o ambiente e o **token GitHub** para acessar os dados dos repositórios.
- Passos para executar os scripts `coletar_repositorios.py` e `coletar_prs.py` para coletar dados sobre Pull Requests.
- Como gerar um **dataset completo** contendo métricas sobre os PRs, como tempo de análise, tamanho e interações.
- Detalhes sobre como realizar análises exploratórias dos dados e testar hipóteses relacionadas aos fatores que influenciam a aceitação de PRs.

---

### 🔹 **[Laboratório 04 - Visualização de Dados com BI](Lab4_)**

**Objetivo:** Utilizar ferramentas de **Business Intelligence (BI)**, como Power BI, Tableau ou Google Data Studio, para criar visualizações interativas dos dados experimentais.

**Instruções na pasta:**
- Definição do **dataset** utilizado, com informações sobre a origem e as métricas relevantes a serem visualizadas.
- Como preparar os dados para importar para a ferramenta de BI escolhida.
- Passos para criar **dashboards** interativos que respondem às questões de pesquisa do laboratório.
- Detalhes sobre como exportar o dashboard final e gerar relatórios que sintetizam as visualizações e insights.

---

### 🔹 **[Laboratório 05 - GraphQL vs REST](Lab5_)**

**Objetivo:** Comparar as tecnologias **GraphQL** e **REST** em termos de desempenho, eficiência no consumo de dados e complexidade de implementação.

**Instruções na pasta:**
- Como configurar os **scripts de teste** para avaliar as APIs REST e GraphQL.
- Passos para realizar experimentos, coletar **tempos de resposta** e medir o **tamanho das respostas**.
- Como analisar os resultados experimentais, aplicando estatísticas descritivas e testes de hipóteses.
- Instruções para visualizar os resultados utilizando gráficos e relatórios comparativos.

---

## 🛠️ **Tecnologias e Ferramentas Utilizadas**

### **Linguagens de Programação e Tecnologias**
- **Python 3.8+ / 3.12**: Linguagem principal utilizada em todos os experimentos para automação, coleta de dados e análise de resultados.
- **GitHub API (GraphQL/REST)**: Utilizada para coletar dados sobre repositórios, Pull Requests, issues e outros dados dos repositórios do GitHub.
- **Java**: Para análise de qualidade de código em repositórios Java no Laboratório 02.

### **Ferramentas de BI**
- **Power BI**: Para criação de dashboards interativos e visualizações dinâmicas de dados experimentais.
- **Tableau**: Ferramenta alternativa para visualização de dados em tempo real.
- **Google Data Studio**: Ferramenta de visualização gratuita do Google, utilizada para criar relatórios e dashboards.

### **Ferramentas e Bibliotecas de Análise de Dados**
- **CK**: Ferramenta para análise de métricas de código Java, utilizada para calcular acoplamento, coesão e complexidade.
- **Pandas**: Biblioteca essencial para manipulação e análise de dados tabulares (CSV, Excel).
- **Matplotlib**: Biblioteca para visualização de dados, gerando gráficos como linhas, barras e dispersões.
- **Seaborn**: Complemento ao **Matplotlib**, facilita a criação de gráficos complexos e estatísticas visuais.
- **Requests**: Biblioteca para fazer requisições HTTP, fundamental para acessar a API do GitHub e coletar dados.
- **GitPython**: Biblioteca para interação com repositórios Git, utilizada no Laboratório 02 para clonar repositórios.
- **Jupyter Notebook**: Ambiente interativo para análise de dados e exploração de resultados.

### **Ferramentas para Análise Estatística e Testes**
- **SciPy**: Para testes estatísticos avançados, como **teste t** e **análises de correlação** (Pearson, Spearman).
- **Statsmodels**: Outra ferramenta para análise estatística que pode ser utilizada para modelagem de dados.

### **Gerenciamento de Ambiente e Dependências**
- **pip**: Gerenciador de pacotes Python utilizado para instalar as dependências necessárias para cada laboratório.
- **virtualenv**: Para criar ambientes isolados para garantir que as dependências não conflitem com outros projetos.
- **dotenv**: Para gerenciar variáveis de ambiente de forma segura, como o **token do GitHub** necessário para a API.

---

## 🛠️ **Bibliotecas Externas Usadas**

1. **Pandas**: Para análise de dados estruturados.
2. **Matplotlib & Seaborn**: Para visualização de gráficos e dados.
3. **Requests**: Para interagir com APIs externas, como a do GitHub.
4. **Dotenv**: Para configuração de variáveis de ambiente (como o **GITHUB_TOKEN**).
5. **GitPython**: Para interagir com repositórios Git programaticamente.
6. **Jupyter Notebook**: Para trabalhar de forma interativa, principalmente na análise de dados e experimentação.
7. **SciPy**: Para realizar testes estatísticos e análises avançadas de dados.
8. **Statsmodels**: Para modelos e testes estatísticos mais complexos.

---

## 📖 **Como Executar os Laboratórios**

Cada laboratório possui instruções detalhadas em seu respectivo **README**. Em geral, os passos para executar são os seguintes:

1. **Clonar o repositório**:
   ```bash
   git clone https://github.com/RubbiaMattos/Lab_Experimentacao_Software_1.2025.git
   cd Lab_Experimentacao_Software_1.2025/[nome_do_laboratorio]
   ```

2. **Instalar as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Executar o script principal**:
   ```bash
   python [script_principal].py
   ```

Cada laboratório contém instruções específicas para a execução completa do experimento, coleta de dados e geração dos resultados.

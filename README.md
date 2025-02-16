# 📊 Laboratório de Experimentação de Software

Este repositório contém uma série de laboratórios realizados na disciplina **Laboratório de Experimentação de Software** do curso de **Engenharia de Software** da **PUC Minas**, ministrada pelo professor **João Paulo Carneiro Aramuni**. Os experimentos exploram boas práticas no desenvolvimento de software, com foco em repositórios open-source e tecnologias emergentes.

---

## 📌 Lista de Laboratórios

### 🔹 [Laboratório 01 - Características de Repositórios Populares](Documentos/LABORATÓRIO_01.pdf)

**Objetivo:**  
Este laboratório tem como objetivo coletar e analisar dados sobre os repositórios mais populares no GitHub. A análise busca entender as características desses repositórios, como sua **maturidade**, **atividade** e **contribuições externas**. As métricas analisadas incluem idade, linguagens de programação, Pull Requests (PRs), releases e issues (problemas).

**Principais Análises:**
- **RQ 01**: Qual a relação entre a idade e a popularidade dos repositórios?
- **RQ 02**: Repositórios populares recebem muitas contribuições externas? (Pull Requests aceitos)
- **RQ 03**: Repositórios populares lançam releases frequentemente? Qual sua estabilidade?
- **RQ 04**: Qual a frequência de atualizações nos repositórios populares?
- **RQ 05**: Quais as principais linguagens de programação utilizadas nos repositórios populares?
- **RQ 06**: Os repositórios populares possuem um alto percentual de issues fechadas?
- **RQ 07**: Como as métricas de contribuições externas, releases e atualizações variam conforme a linguagem utilizada?

**Implementação - Lab01S01:**  
Este laboratório utiliza **GraphQL** para coletar dados sobre os 100 repositórios mais populares no GitHub. O processo é automatizado, eliminando a necessidade de bibliotecas externas para realizar chamadas à API.

### Funcionalidades:
- **Consulta GraphQL** para coletar dados dos 100 repositórios mais populares do GitHub.
- Coleta de **métricas essenciais**, incluindo:
  - **Idade do repositório** (data de criação).
  - **Total de Pull Requests aceitos**.
  - **Número de releases** do repositório.
  - **Data da última atualização**.
  - **Linguagem primária** utilizada.
  - **Percentual de issues fechadas** como indicador de manutenção ativa.
- **Armazenamento dos dados** em um arquivo **CSV**.
- **Requisição automática** para coleta de dados via API do GitHub sem dependências externas.

### Estrutura do Diretório:
```
📂 Lab1_RepoPop
 ├── 📂 Lab01S01  → Consulta GraphQL para 100 repositórios + requisição automática
 │   ├── 📜 .env.config
 │   ├── 📂 Relatórios
 │   │   ├── 📄 Análise de Repositórios Populares no GitHub.docx
 │   │   ├── 📄 Análise de Repositórios Populares no GitHub.pdf
 │   │   ├── 📊 github_analysis.csv
 │   │   ├── 📊 qtd_PRs_aceitos.png
 │   │   ├── 📊 top_languages.png
 │   ├── 🐍 RepoPop100.py
 ├── 📂 Lab01S02  → Paginação para 1000 repositórios + dados em CSV + hipóteses iniciais
 ├── 📂 Lab01S03  → Análise e visualização de dados + elaboração do relatório final
```

### 🔑 Arquivo de Configuração:
O arquivo `.env.config` contém a variável `GITHUB_TOKEN`, que deve ser configurada com um token de autenticação válido da API do GitHub para permitir a coleta de dados.

### Como Executar:

1. **Clone o repositório**:
   No terminal, clone o repositório e acesse o diretório onde o script será executado:
   ```bash
   git clone https://github.com/RubbiaMattos/Lab_Experimentacao_Software_1.2025.git
   cd Lab_Experimentacao_Software_1.2025/Lab1_RepoPop/Lab01S01
   ```

2. **Configure o token de autenticação**:
   Abra o arquivo `.env.config` e substitua o valor de `GITHUB_TOKEN` com um token de autenticação do GitHub válido:
   ```env
   GITHUB_TOKEN=seu_novo_token_aqui
   ```

3. **Instale as dependências**:
   Instale as bibliotecas necessárias para rodar o script:
   ```bash
   py -3.12 -m pip install pandas requests matplotlib seaborn python-dotenv
   ```

4. **Execute o script**:
   Execute o script Python para iniciar a coleta de dados e gerar os relatórios:
   ```bash
   python RepoPop100.py
   ```

### Resultados:
Após a execução do script, os seguintes arquivos serão gerados na pasta `Relatórios`:

- **`github_analysis.csv`**: Arquivo CSV contendo todos os dados coletados, como número de PRs, releases, idade do repositório, etc.
- **`qtd_PRs_aceitos.png`**: Gráfico de barras mostrando a distribuição do número de Pull Requests aceitos nos repositórios.
- **`top_languages.png`**: Gráfico de barras exibindo as 10 linguagens de programação mais utilizadas nos repositórios populares.

Esses arquivos podem ser visualizados usando ferramentas como **Excel**, **Google Sheets** ou **Python**, e usados para análise e geração de insights.

### 🔄 Próximas Etapas:
- **Lab01S02**: Implementação de paginação para coletar dados de até **1000 repositórios**, além da análise inicial das métricas.
- **Lab01S03**: Análise e visualização dos dados coletados, com elaboração do relatório final e aprofundamento na análise estatística dos dados.

---

### 🔹 [Laboratório 02 - Qualidade de Sistemas Java](Documentos/LABORATÓRIO_02.pdf)

**Objetivo:**  
Analisar a qualidade do código em repositórios Java open-source, utilizando métricas como **acoplamento**, **coesão** e **complexidade**.

**Principais Análises:**
- Medição do acoplamento entre classes usando **CBO** (Coupling Between Objects).
- Avaliação da herança por meio da métrica **DIT** (Depth of Inheritance Tree).
- Análise da coesão entre métodos usando **LCOM** (Lack of Cohesion of Methods).
- Correlação entre a popularidade do repositório e a qualidade do código.
- Influência da frequência de commits e releases na legibilidade e modularidade do código.

**Estrutura do Diretório:**
```
📂 Lab2
 ├── 📂 Lab02S01  → Coleta de Dados e Extração de Métricas
 ├── 📂 Lab02S02  → Análise Estatística e Visualização de Dados
 ├── 📂 Lab02S03  → Relatório Final e Conclusões
```

---

### 🔹 [Laboratório 03 - Code Review no GitHub](Documentos/LABORATÓRIO_03.pdf)

**Objetivo:**  
Analisar a atividade de **code review** em repositórios populares do GitHub e identificar os fatores que influenciam a aceitação ou rejeição de **Pull Requests (PRs)**.

**Principais Análises:**
- Relação entre o tamanho dos PRs e seu feedback final (aprovado/rejeitado).
- Impacto do tempo de análise dos PRs no feedback final.
- Influência da descrição dos PRs na aceitação ou rejeição.
- Correlação entre interações nos PRs e a decisão final do revisor.

**Estrutura do Diretório:**
```
📂 Lab3
 ├── 📂 Lab03S01  → Seleção de repositórios + Script de coleta de PRs  
 ├── 📂 Lab03S02  → Dataset completo + Hipóteses iniciais  
 ├── 📂 Lab03S03  → Análise dos dados + Relatório final  
```

---

### 🔹 [Laboratório 04 - Visualização de Dados com BI](Documentos/LABORATÓRIO_04.pdf)

**Objetivo:**  
Utilizar ferramentas de **Business Intelligence (BI)** para transformar dados experimentais em visualizações interativas e acessíveis.

**Principais Análises:**
- Construção de dashboards dinâmicos para análise de dados experimentais.
- Comparação de diferentes formas de visualização para otimizar a interpretação dos dados.
- Aplicação de técnicas de sumarização e filtragem para extrair insights relevantes.
- Demonstração de como a visualização de dados pode auxiliar na tomada de decisões em engenharia de software.

**Estrutura do Projeto:**
```
📂 Lab4
 ├── 📂 Lab04S01  → Caracterização do Dataset 
 ├── 📂 Lab04S02  → Visualizações para as Questões de Pesquisa 
 ├── 📂 Lab04S03  → Dashboard Final + Relatório 
```

---

### 🔹 [Laboratório 05 - GraphQL vs REST](Documentos/LABORATÓRIO_05.pdf)

**Objetivo:**  
Comparar as tecnologias **GraphQL** e **REST** em termos de desempenho, eficiência no consumo de dados e complexidade de implementação.

**Principais Análises:**
- Comparação do tempo de resposta entre **GraphQL** e **REST**.
- Análise do tamanho dos dados e ocorrência de **overfetching** e **underfetching**.
- Avaliação de como **GraphQL** pode ser mais eficiente no consumo de dados em comparação com **REST**.

**Estrutura do Projeto:**
```
📂 Lab5
 ├── 📂 Lab05S01  → Desenho e Preparação do Experimento
 ├── 📂 Lab05S02  → Execução e Análise dos Resultados
 ├── 📂 Lab05S03  → Criação do Dashboard de Visualização 
```

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.12**: Linguagem principal.
- **Git e GitHub**: Controle de versão e repositório.
- **GraphQL**: Tecnologia para consultas otimizadas na API do GitHub.

---

## 🛠️ Bibliotecas Externas

- **Pandas**: Manipulação e análise de dados.
- **Matplotlib & Seaborn**: Visualização de dados.
- **Requests**: Requisições HTTP para API do GitHub.
- **Dotenv**: Gerenciamento de variáveis de ambiente.
- **Jupyter Notebook**: Ambiente interativo para análise de dados.

---

## 📖 Referências

- [Documentação do GitHub](https://docs.github.com/pt)
- [Octoverse - GitHub Insights](https://octoverse.github.com/)
- [GraphQL vs REST](https://graphql.org/learn/)

---

## 👥 Equipe

- **Nataniel Geraldo Mendes Peixoto**
- **Nelson de Campos Nolasco**
- **Rúbia Coelho de Matos**

**Professor:** João Paulo Carneiro Aramuni  
**Curso:** Engenharia de Software  
**Disciplina:** Laboratório de Experimentação de Software  
**Instituição:** Pontifícia Universidade Católica de Minas Gerais (PUC Minas)
# 📌 **Laboratório 01 - Características de Repositórios Populares**

## 🎯 **Objetivo**

Este laboratório analisa repositórios populares no **GitHub**, investigando sua **maturidade, atividade e engajamento**. Utilizamos **GraphQL** para coletar dados e gerar insights sobre métricas como **idade do repositório, contribuições externas, releases e issues fechadas**.

---

## 🔎 **Questões de Pesquisa**

1️⃣ **Sistemas populares são antigos?** *(Idade do repositório)*\
2️⃣ **Recebem muitas contribuições externas?** *(PRs aceitos)*\
3️⃣ **Lançam releases com frequência?** *(Número total de releases)*\
4️⃣ **São atualizados regularmente?** *(Tempo desde a última atualização)*\
5️⃣ **São escritos em linguagens populares?** *(Linguagem primária usada)*\
6️⃣ **Possuem alto percentual de issues fechadas?** *(Proporção entre issues abertas e fechadas)*\
7️⃣ **Linguagens populares influenciam PRs, releases e atualizações?** *(Comparação entre linguagens e métricas)*

---

## 📂 **Estrutura do Projeto**

```
📂 Lab1_RepoPop
├─ 📂 Lab01S01 *(Sprint 1: Coleta Inicial - 100 Repositórios)*
│  ├─ 🐍 RepoPop100.py *(Script inicial - coleta de 100 repositórios)*
│  ├─ 📂 Relatórios *(Saída de dados - 100 repositórios)*
│  │  ├─ 📄 Análise_de_Repositórios_Populares.docx *(Relatório inicial)*
│  │  ├─ 📄 Análise_de_Repositórios_Populares.pdf *(Versão PDF)*
│  │  ├─ 📊 github_analysis_S01.csv *(Dados coletados)*
│  │  ├─ 📊 qtd_PRs_aceitos_S01.png *(Distribuição de PRs aceitos)*
│  │  ├─ 📊 top_languages_S01.png *(Linguagens mais usadas)*
│
├─ 📂 Lab01S02 *(Sprint 2: Expansão - 1000 Repositórios + Hipóteses Iniciais)*
│  ├─ 🐍 RepoPop1000.py *(Script atualizado com paginação para 1000 repositórios)*
│  ├─ 📂 Relatórios *(Saída de dados - 1000 repositórios + primeiras análises)*
│  │  ├─ 📄 Análise_de_Repositórios_Populares.docx *(Relatório expandido)*
│  │  ├─ 📄 Análise_de_Repositórios_Populares.pdf *(Versão PDF)*
│  │  ├─ 📊 github_analysis_S02.csv *(Dados coletados)*
│  │  ├─ 📊 qtd_PRs_aceitos_S02.png *(Gráfico atualizado de PRs aceitos)*
│  │  ├─ 📊 top_languages_S02.png *(Gráfico atualizado das linguagens mais usadas)*
│
├─ 📂 Lab01S03 *(Sprint 3: Análise Final e Relatório Completo)*
│  ├─ 🐍 RepoPop1000Final.py *(Script final de análise e visualização)*
│  ├─ 📂 Relatórios *(Relatório consolidado e gráficos finais)*
│  │  ├─ 📂 Figuras *(Visualizações geradas no relatório final)*
│  │  │  ├─ 📊 dias_desde_ultima_atualizacao.png *(Tempo desde a última atualização)*
│  │  │  ├─ 📊 idade_repositorios.png *(Distribuição da idade dos repositórios)*
│  │  │  ├─ 📊 metricas_por_linguagem.png *(Métricas por linguagem)*
│  │  │  ├─ 📊 percentual_issues_fechadas.png *(Proporção de issues fechadas)*
│  │  │  ├─ 📊 qtd_PRs_aceitos_S03.png *(Distribuição de PRs aceitos - versão final)*
│  │  │  ├─ 📊 qtd_releases.png *(Distribuição de releases)*
│  │  │  ├─ 📊 top_languages_S03.png *(Linguagens mais populares - versão final)*
│  │  ├─ 📄 Análise_de_Repositórios_Populares.pptx *(Apresentação dos resultados)*
│  │  ├─ 📄 Análise_de_Repositórios_Populares.docx *(Versão final do relatório)*
│  │  ├─ 📄 Análise_de_Repositórios_Populares.pdf *(Documento final)*
│  │  ├─ 📊 github_analysis_S03.csv *(Dados finais analisados)*
│
├─ 📜 README_Lab1.md *(Arquivo explicativo)*
└─ 📜 env.config *(Configuração do token GitHub na raiz do projeto)*
```

---

Ótimo! Seguindo a sua instrução, o caminho do arquivo `env.config` de todos os laboratórios será atualizado para:

```
LABORATÓRIO DE EXPERIMENTAÇÃO DE SOFTWARE\Lab_Experimentacao_Software_1.2025\env.config
```

✅ Aqui está o texto padrão atualizado para cada README onde for necessário configurar o `env.config`:

---

## 🔑 **Configuração do Token da API GitHub**

Para acessar a API do GitHub, é necessário configurar um **token de autenticação**. O token deve ser armazenado no arquivo:

```
LABORATÓRIO DE EXPERIMENTAÇÃO DE SOFTWARE\Lab_Experimentacao_Software_1.2025\env.config
```

com o seguinte conteúdo:

```
GITHUB_TOKEN=seu_token_aqui
```

### Como obter o Token do GitHub:
1. Acesse [GitHub Developer Settings](https://github.com/settings/tokens).
2. Clique em **Generate new token (classic)**.
3. Selecione as permissões:
   - `repo` → Acesso a repositórios públicos
   - `read:org` → (se necessário)
4. Gere o token e adicione ao arquivo `env.config`.

**⚠️ Importante:** Nunca compartilhe seu token publicamente.

---

Posso agora **aplicar** este trecho e ajuste nos READMEs dos laboratórios 1, 2, 3, 4 e 5. Quer que eu gere o conteúdo final atualizado de cada um ou você quer apenas o padrão mesmo? Posso montar e te devolver os READMEs atualizados se preferir!

---

## 🚀 **Sprints do Projeto**

### 📌 **Sprint 1 - Coleta Inicial (100 Repositórios)**

#### 🔧 **Implementação**

- Desenvolvimento do script inicial com GraphQL para obter os **100 repositórios mais populares**.
- Implementação utilizando **Python** e a biblioteca **requests** para comunicação com a API GitHub.
- **Armazenamento dos dados coletados** em um arquivo CSV para análise posterior.

#### ⚙️ **Funcionalidades**

✔ Coleta de **idade do repositório, PRs aceitos, releases e linguagem primária**.\
✔ Consulta automatizada utilizando a API do GitHub via GraphQL.\
✔ Armazenamento dos dados no formato CSV.

#### 📦 **Dependências**

- **Python 3.8+**
- `requests`, `pandas`, `python-dotenv`

#### ▶️ **Como Executar**

1️⃣ **Clone o repositório:** No terminal, clone o repositório e acesse o diretório onde o script será executado:

```bash
git clone https://github.com/RubbiaMattos/Lab_Experimentacao_Software_1.2025.git
cd Lab_Experimentacao_Software_1.2025/Lab1_RepoPop
```

2️⃣ **Instale as dependências:** Instale as bibliotecas necessárias para rodar o script:

```bash
py -3.12 -m pip install pandas requests matplotlib seaborn python-dotenv
```

3️⃣ **Execute o script:** Inicie a coleta de dados e gere os relatórios:

```bash
python Lab1_RepoPop/Lab01S01/RepoPop100.py
```

📊 **Resultados:**\
✔ `github_analysis.csv` → Dados coletados dos 100 repositórios.\
✔ `qtd_PRs_aceitos.png` → Gráfico da distribuição de PRs aceitos.\
✔ `top_languages.png` → Gráfico das linguagens mais usadas.\
✔ `Análise_de_Repositórios_Populares.pdf` → Relatório inicial.

---

### 📌 **Sprint 2 - Expansão (1000 Repositórios + Hipóteses Iniciais)**

#### 🔧 **Implementação**

- Expansão da coleta de dados para **1000 repositórios** utilizando paginação na API GraphQL.
- Desenvolvimento de **hipóteses iniciais** com base na análise dos primeiros 100 repositórios.
- Criação de gráficos preliminares para visualizar padrões e tendências nos dados coletados.

#### ⚙️ **Funcionalidades**

✔ Implementação da **paginação GraphQL** para acessar até **1000 repositórios**.\
✔ Geração de um arquivo CSV com os dados coletados.\
✔ Criação de gráficos exploratórios.

#### 📦 **Dependências**

- **Todas as dependências da Sprint 1**
- `matplotlib`, `seaborn`

#### ▶️ **Como Executar**

1️⃣ **Clone o repositório:** No terminal, clone o repositório e acesse o diretório onde o script será executado:

```bash
git clone https://github.com/RubbiaMattos/Lab_Experimentacao_Software_1.2025.git
cd Lab_Experimentacao_Software_1.2025/Lab1_RepoPop
```

2️⃣ **Instale as dependências:** Instale as bibliotecas necessárias para rodar o script:

```bash
py -3.12 -m pip install pandas requests matplotlib seaborn python-dotenv
```

3️⃣ **Execute o script:** Execute o script para iniciar a coleta de dados e geração dos relatórios:

```bash
python Lab1_RepoPop/Lab01S02/RepoPop1000.py
```

📊 **Resultados:**\
✔ `github_analysis.csv` → Dados expandidos para 1000 repositórios.\
✔ `qtd_PRs_aceitos.png` → Gráfico atualizado de PRs aceitos.\
✔ `top_languages.png` → Gráfico atualizado das linguagens mais populares.\
✔ `Análise de Repositórios Populares.pdf` → Relatório inicial com hipóteses.

---

### 📌 **Sprint 3 - Análise Final e Relatório Completo**

#### 🔧 **Implementação**

- **Análise estatística aprofundada** das métricas coletadas, identificando padrões e correlações.
- **Geração de gráficos e tabelas detalhadas** para ilustrar os resultados obtidos.
- **Criação do relatório final consolidado**, documentando todas as descobertas e insights do estudo.

#### 📦 **Dependências**

- **Todas as dependências da Sprint 2**
- `scipy`, `numpy`

#### ▶️ **Como Executar**

1️⃣ **Clone o repositório:** No terminal, clone o repositório e acesse o diretório onde o script será executado:

```bash
git clone https://github.com/RubbiaMattos/Lab_Experimentacao_Software_1.2025.git
cd Lab_Experimentacao_Software_1.2025/Lab1_RepoPop
```

2️⃣ **Instale as dependências:** Instale as bibliotecas necessárias para rodar o script:

```bash
py -3.12 -m pip install pandas requests matplotlib seaborn python-dotenv
```

3️⃣ **Execute o script:** Inicie a coleta de dados e gere os relatórios:

```bash
python Lab1_RepoPop/Lab01S03/RepoPop1000Final.py
```

📊 **Resultados:**\
✔ `github_analysis.csv` → Dados finais analisados.\
✔ `qtd_PRs_aceitos.png` → PRs aceitos na versão final.\
✔ `qtd_releases.png` → Distribuição de releases.\
✔ `dias_desde_ultima_atualizacao.png` → Tempo desde a última atualização.\
✔ `idade_repositorios.png` → Distribuição da idade dos repositórios.\
✔ `percentual_issues_fechadas.png` → Percentual de issues fechadas.\
✔ `metricas_por_linguagem.png` → Comparação das métricas por linguagem.\
✔ `Análise_de_Repositórios_Populares.pdf` → Relatório final consolidado.\
✔ `Análise_de_Repositórios_Populares.pptx` → Apresentação final dos resultados.

---

## 📢 **Equipe do Projeto**

👥 **Nataniel Geraldo Mendes Peixoto**\
👥 **Nelson de Campos Nolasco**\
👥 **Rubia Coelho de Matos**

# 📌 **Laboratório 02 - Qualidade de Sistemas Java**

## 🎯 **Objetivo**

Este laboratório tem como objetivo **analisar a qualidade de repositórios Java open-source**, correlacionando métricas de qualidade do código com características do processo de desenvolvimento. Utilizaremos a ferramenta **CK** para extrair métricas de acoplamento, herança e coesão, além de coletar dados sobre popularidade, maturidade e atividade dos repositórios.

---

## 🔎 **Questões de Pesquisa**

1️⃣ **Qual a relação entre a popularidade dos repositórios e suas características de qualidade?** *(Número de estrelas vs. métricas de código)*\
2️⃣ **Qual a relação entre a maturidade dos repositórios e suas características de qualidade?** *(Idade do repositório vs. métricas de código)*\
3️⃣ **Qual a relação entre a atividade dos repositórios e suas características de qualidade?** *(Número de releases vs. métricas de código)*\
4️⃣ **Qual a relação entre o tamanho dos repositórios e suas características de qualidade?** *(Linhas de código vs. métricas de código)*

---

## 📂 **Estrutura do Projeto**

```
📂 Lab2_QualiJava
├─ 📂 Lab2S01 *(Sprint 1: Coleta e análise de dados)*
│  ├─ 📂 data *(Repositórios clonados e dados extraídos)*
│  │  ├─ 📂 ck_output_LeetCodeAnimation *(Ferramenta de análise de código)*
│  │  │  ├─  📄 class.csv *(Dados sobre classes Java extraídos pelo CK)*
│  │  │  ├─ 📄 field.csv *(Dados sobre atributos extraídos pelo CK)*
│  │  │  ├─ 📄 method.csv *(Dados sobre métodos extraídos pelo CK)*
│  │  │  ├─ 📄 variable.csv *(Dados sobre variáveis extraídas pelo CK)*
│  │  ├─ 📂 repos *(Repositórios clonados para análise)*
│  │  │  ├─ 📂 LeetCodeAnimation *(Exemplo de repositório clonado)*
│  │  │  │  ├─ 📄 repositorios_list.csv *(Lista dos repositórios coletados)*
│  │  │  │  ├─ 📄 resultados_totais.csv *(Métricas extraídas dos repositórios)*
│  ├─ 📄 ck.jar *(Ferramenta CK para análise de código Java)*
│  ├─ 🐍 coleta_repositorios.py *(Coleta os 1000 repositórios mais populares em Java)*
│  ├─ 🐍 automacao_clone.py *(Clona os repositórios coletados)*
│  ├─ 🐍 coletar_dados.py *(Executa a ferramenta CK e coleta métricas dos repositórios)*
│  ├─ 🐍 analisar_dados.py *(Analisa as métricas coletadas e gera os resultados)*
│  ├─ 🐍 main.py *(Pipeline completo do laboratório)*
│
├─ 📂 Lab2S02 *(Sprint 2: Relatório Final e Documentação)*
│  ├─ 📂 Docs *(Relatórios e arquivos auxiliares)*
│  │  ├─ 📜 relatório_final.txt *(Relatório final do laboratório)*
│
├─ 📜 LABORATÓRIO_02.pdf *(Descrição da atividade)*
├─ 📜 README_Lab2.md *(Arquivo explicativo do laboratório)*
├─ 📜 .env.config *(Configuração do token GitHub e variáveis do projeto)*
```

---

## 🔑 **Configuração do Token da API GitHub**

Para acessar a API do GitHub, é necessário configurar um **token de autenticação**. O token deve ser armazenado em um arquivo `.env.config` na raiz do projeto, com o seguinte formato:

```
GITHUB_TOKEN=seu_token_aqui
```

### Como obter um Token do GitHub:
1. Acesse [GitHub Developer Settings](https://github.com/settings/tokens).
2. Clique em **Generate new token (classic)**.
3. Selecione as permissões necessárias:
   - `repo` (acesso a repositórios públicos)
   - `read:org` (para ler informações de organizações, se necessário)
4. Gere o token e copie-o.
5. Cole o token no arquivo `.env.config`.

**Importante:** Nunca compartilhe seu token publicamente para evitar riscos de segurança.

---

## 🚀 **Sprints do Projeto**

### 📌 **Sprint 1 - Coleta de Dados e Análise Inicial**

#### 🔧 **Implementação**
- Coleta dos 1000 repositórios Java mais populares via **API REST do GitHub**.
- Clonagem automática dos repositórios coletados.
- Extração de métricas de código usando a ferramenta **CK**.
- Organização e armazenamento das métricas para posterior análise.

#### 📦 **Dependências**
- **Python 3.8+**
- `requests`, `pandas`, `python-dotenv`, `gitpython`

Segue a atualização do **Como Executar** para a Sprint 1, garantindo que os scripts sejam executados na ordem correta:

---

#### ▶️ **Como Executar**

1️⃣ **Clone o repositório:**

```bash
git clone https://github.com/RubbiaMattos/Lab_Experimentacao_Software_1.2025.git
cd Lab_Experimentacao_Software_1.2025/Lab2_QualiJava
```

2️⃣ **Instale as dependências:**

```bash
pip install requests pandas python-dotenv gitpython
```

3️⃣ **Executando os scripts na ordem correta:**

- **Coleta dos repositórios:**  
  Gere o arquivo com as URLs dos repositórios (caso ainda não exista) executando:
  
  ```bash
  python coleta_repositorios.py
  ```

- **Clonagem dos repositórios:**  
  Clone os repositórios listados no arquivo gerado:

  ```bash
  python automacao_clone.py
  ```

- **Coleta das métricas:**  
  Após a clonagem, extraia as métricas utilizando a ferramenta CK:

  ```bash
  python coletar_dados.py
  ```
  
  Este script gera o arquivo `resultados_totais.csv` com as métricas extraídas.

- **Análise dos dados:**  
  Finalmente, processe e analise os dados consolidados executando:

  ```bash
  python analisar_dados.py
  ```

> **Atenção:** O script de análise (**analisar_dados.py**) deve ser rodado somente após os repositórios terem sido clonados e os dados consolidados coletados com sucesso.

---

#### 📊 **Resultados**

- **Organização do Projeto:**  
  O diretório **Lab2_QualiJava** está estruturado para separar as atividades de cada sprint. Em particular, a Sprint 1 está organizada dentro do diretório **Lab2S01**, que contém:

  - **data:**  
    - **ck_output_LeetCodeAnimation:**  
      Aqui são armazenados os dados extraídos pela ferramenta CK, contendo:
      - **class.csv:** Informações sobre as classes Java.
      - **field.csv:** Dados dos atributos extraídos.
      - **method.csv:** Métricas referentes aos métodos.
      - **variable.csv:** Informações sobre as variáveis do código.
      
    - **repos:**  
      Contém os repositórios clonados para análise. Por exemplo, no subdiretório **LeetCodeAnimation** encontramos:
      - **repositorios_list.csv:** Lista dos repositórios coletados via API do GitHub.
      - **resultados_totais.csv:** Arquivo consolidado com as métricas extraídas dos repositórios.

- **Etapas e Resultados Concretos:**

  - **Coleta dos Repositórios:**  
    Foram coletados 1000 repositórios Java por meio da API do GitHub. As URLs desses repositórios foram armazenadas no arquivo `repositorios_list.csv`, localizado no diretório correspondente.

  - **Clonagem dos Repositórios:**  
    Todos os repositórios coletados foram clonados com sucesso para a pasta `data/repos`, permitindo o acesso local necessário para a análise.

  - **Extração de Métricas:**  
    Utilizando a ferramenta CK, os dados referentes à qualidade do código (como acoplamento, herança, coesão e demais métricas) foram extraídos dos repositórios clonados. Os resultados detalhados foram salvos nos arquivos CSV dentro da pasta `data/ck_output_LeetCodeAnimation`, e um arquivo consolidado, `resultados_totais.csv`, foi gerado para facilitar a análise.

---

### 📌 **Sprint 2 - Análise de Métricas e Hipóteses**

#### 🔧 **Implementação**
- Análise exploratória das métricas coletadas.
- Desenvolvimento de hipóteses sobre as correlações entre popularidade, maturidade, atividade e qualidade do código.
- Geração de gráficos para visualizar tendências e padrões nos dados coletados.

#### 📦 **Dependências**
- **Todas as dependências da Sprint 1**
- `matplotlib`, `seaborn`

#### ▶️ **Como Executar**

```bash
python analisar_dados.py
```

#### 📊 **Resultados**
✔ Expansão dos dados para 1000 repositórios coletados.
✔ Gráficos preliminares das métricas coletadas.
✔ Análise inicial de correlação entre métricas.
✔ Desenvolvimento de hipóteses sobre os padrões identificados.

---

## 🔜 **Próximos Passos**

1️⃣ **Aprimorar a análise estatística** das métricas coletadas, incluindo testes de correlação mais robustos (Spearman ou Pearson).
2️⃣ **Gerar gráficos de correlação mais detalhados** para identificar tendências entre as métricas coletadas.
3️⃣ **Explorar novas métricas** além do CK, para obter uma visão mais ampla da qualidade do código.
4️⃣ **Comparar os resultados com benchmarks conhecidos** e estudos prévios sobre qualidade de software.
5️⃣ **Preparação para apresentação final**, refinando os insights e documentando os principais achados.

---

## 📢 **Equipe do Projeto**

👥 **Nataniel Geraldo Mendes Peixoto**\
👥 **Nelson de Campos Nolasco**\
👥 **Rubia Coelho de Matos**
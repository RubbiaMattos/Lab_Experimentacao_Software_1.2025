Aqui está o **README completo e atualizado** do projeto, considerando a estrutura organizada e o planejamento para a **Sprint 2**.  

---

# 📌 **Laboratório 02 - Qualidade de Sistemas Java**  

## 🎯 **Objetivo**  

Este laboratório tem como objetivo **avaliar a qualidade de repositórios Java open-source**, analisando métricas de código e características do desenvolvimento. Utilizaremos a ferramenta **CK** para extrair métricas como **acoplamento, herança e coesão**, além de coletar dados sobre **popularidade, maturidade e atividade dos repositórios**.  

---

## 🔎 **Questões de Pesquisa**  

1️⃣ **Popularidade x Qualidade** → Repositórios com mais estrelas têm código de melhor qualidade?  
2️⃣ **Maturidade x Qualidade** → Projetos mais antigos são mais bem estruturados?  
3️⃣ **Atividade x Manutenibilidade** → Repositórios mais ativos têm código mais modular?  
4️⃣ **Tamanho x Complexidade** → Repositórios maiores possuem mais acoplamento e menor coesão?  

---

## 📂 **Estrutura do Projeto**  

```
📂 Lab2_QualiJava  
├─ 📂 Lab2S01 *(Sprint 1: Coleta e análise de dados)*  
│  ├─ 📂 data *(Dados coletados e repositórios clonados)*  
│  │  ├─ 📂 ck_output *(Métricas extraídas pelo CK)*  
│  │  │  ├─ 📄 class.csv *(Dados sobre classes Java)*  
│  │  │  ├─ 📄 field.csv *(Atributos extraídos pelo CK)*  
│  │  │  ├─ 📄 method.csv *(Métricas sobre métodos)*  
│  │  │  ├─ 📄 variable.csv *(Informações sobre variáveis)*  
│  │  ├─ 📂 repos *(Repositórios clonados para análise)*  
│  │  ├─ 📄 repositorios_list.csv *(Lista dos repositórios coletados)*  
│  │  ├─ 📄 resultados_totais.csv *(Métricas extraídas dos repositórios)*  
│  │  ├─ 📄 matriz_correlacao.png *(Gráfico de correlação das métricas)*  
│  │  ├─ 📄 analise_metrica_ck.csv *(Resumo estatístico das métricas)*  
│  ├─ 📄 ck.jar *(Ferramenta CK para análise de código Java)*  
│  ├─ 🐍 coleta_repositorios.py *(Coleta repositórios via API GitHub)*  
│  ├─ 🐍 automacao_clone.py *(Clona os repositórios listados)*  
│  ├─ 🐍 coletar_dados.py *(Executa a ferramenta CK e coleta métricas)*  
│  ├─ 🐍 analisar_dados.py *(Processa e analisa os dados coletados)*  
│  ├─ 🐍 main.py *(Pipeline completo do laboratório)*  
│
├─ 📂 Lab2S02 *(Sprint 2: Relatório Final e Documentação)*  
│  ├─ 📂 Docs *(Relatórios e arquivos auxiliares)*  
│  │  ├─ 📜 relatório_final.txt *(Relatório final do laboratório)*  
│
├─ 📜 LABORATÓRIO_02.pdf *(Descrição da atividade)*  
├─ 📜 README_Lab2.md *(Instruções detalhadas do laboratório)*  
├─ 📜 .env.config *(Configuração do token GitHub e variáveis do projeto)*  
```

---

## 🔑 **Configuração do Token da API GitHub**  

O script de coleta requer um **token de autenticação** do GitHub. O token pode ser configurado automaticamente via terminal ou salvo em um arquivo `.env.config` na raiz do projeto, no seguinte formato:

```
GITHUB_TOKEN=seu_token_aqui
```

Caso precise gerar um token, siga os passos:  
1. Acesse [GitHub Developer Settings](https://github.com/settings/tokens).  
2. Clique em **"Generate new token (classic)"**.  
3. Selecione as permissões:  
   - `repo` → Acesso a repositórios públicos  
   - `read:org` → Acesso a informações organizacionais (se necessário)  
4. Copie o token gerado e adicione ao projeto.  

---

## 🚀 **Sprints do Projeto**  

### 📌 **Sprint 1 - Coleta de Dados e Análise Inicial**  

🔹 **Objetivos:**  
- Coletar **1000 repositórios Java** populares via **API do GitHub**.  
- Clonar os repositórios coletados automaticamente.  
- Extrair métricas de código usando a ferramenta **CK**.  
- Organizar e armazenar os dados coletados para análise.  

🔹 **Dependências:**  
```bash
pip install requests pandas python-dotenv gitpython matplotlib seaborn
```

### ▶️ **Como Executar**  

1️⃣ **Clone o repositório:**  
```bash
git clone https://github.com/RubbiaMattos/Lab_Experimentacao_Software_1.2025.git
cd Lab_Experimentacao_Software_1.2025/Lab2_QualiJava
```

2️⃣ **Execute todo o pipeline:**  
```bash
python main.py --step all
```

✅ Coleta dos repositórios via API  
✅ Clonagem dos repositórios listados  
✅ Coleta de métricas de qualidade do código  
✅ Análise inicial dos dados coletados  

---

### 📊 **Resultados da Sprint 1**  

📂 **Lab2S01/data/** gerou os seguintes arquivos:  
- **📂 ck_output/** → Métricas extraídas pelo CK (**class.csv, method.csv, field.csv, variable.csv**).  
- **📂 repos/** → Repositórios clonados para análise.  
- **📄 repositorios_list.csv** → Lista dos 1000 repositórios Java coletados.  
- **📄 resultados_totais.csv** → Consolidação das métricas extraídas.  
- **📄 matriz_correlacao.png** → Gráfico de correlação das métricas.  
- **📄 analise_metrica_ck.csv** → Estatísticas descritivas.  

🔹 **Principais Insights:**  
📌 Possível relação entre **tamanho do código (LOC)** e **acoplamento (CBO)**.  
📌 Projetos **mais antigos** tendem a apresentar **menor coesão (LCOM alto)**.  
📌 Repositórios **mais populares** podem ter código de **melhor qualidade**.  

🚀 *Próximos passos na Sprint 2: análise detalhada e geração de relatórios!*  

---

### 📌 **Sprint 2 - Planejamento e Próximos Passos**  

🔹 **Objetivos:**  
- Revisão e organização dos dados coletados.  
- Definição de hipóteses e padrões a serem analisados.  
- Aplicação de estatísticas e cálculos de correlação entre métricas.  
- Geração de gráficos e relatórios detalhados.  

🔹 **O que será feito?**  
1️⃣ **Revisão e limpeza dos dados** → Verificar inconsistências e outliers.  
2️⃣ **Definição de hipóteses** → Como maturidade, popularidade e qualidade do código se relacionam?  
3️⃣ **Geração de estatísticas e gráficos** → Correlações, distribuições e padrões.  
4️⃣ **Documentação dos resultados** → Criar um relatório consolidando insights.  

🔹 **Ferramentas e Bibliotecas:**  
- **Linguagem:** Python 3.8+  
- **Bibliotecas:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`  

---

## 📢 **Equipe do Projeto**  

👥 **Nataniel Geraldo Mendes Peixoto**  
👥 **Nelson de Campos Nolasco**  
👥 **Rubia Coelho de Matos**  

Aqui está o **README completo e atualizado** do projeto, considerando a estrutura organizada e o planejamento para a **Sprint 2**.  

---

# 📌 **Laboratório 02 - Qualidade de Sistemas Java**  

## 🎯 **Objetivo**  

Este laboratório tem como objetivo **avaliar a qualidade de repositórios Java open-source**, analisando métricas de código e características do desenvolvimento. Utilizaremos a ferramenta **CK** para extrair métricas como **acoplamento, herança e coesão**, além de coletar dados sobre **popularidade, maturidade e atividade dos repositórios**.  

---

## 🔎 **Questões de Pesquisa**  

1️⃣ **Popularidade x Qualidade** → Repositórios com mais estrelas têm código de melhor qualidade?  
2️⃣ **Maturidade x Qualidade** → Projetos mais antigos são mais bem estruturados?  
3️⃣ **Atividade x Manutenibilidade** → Repositórios mais ativos têm código mais modular?  
4️⃣ **Tamanho x Complexidade** → Repositórios maiores possuem mais acoplamento e menor coesão?  

---

## 📂 **Estrutura do Projeto**  

```
📂 Lab2_QualiJava  
├─ 📂 Lab2S01 *(Sprint 1: Coleta e análise de dados)*  
│  ├─ 📂 data *(Dados coletados e repositórios clonados)*  
│  │  ├─ 📂 ck_output *(Métricas extraídas pelo CK)*  
│  │  │  ├─ 📄 class.csv *(Dados sobre classes Java)*  
│  │  │  ├─ 📄 field.csv *(Atributos extraídos pelo CK)*  
│  │  │  ├─ 📄 method.csv *(Métricas sobre métodos)*  
│  │  │  ├─ 📄 variable.csv *(Informações sobre variáveis)*  
│  │  ├─ 📂 repos *(Repositórios clonados para análise)*  
│  │  ├─ 📄 repositorios_list.csv *(Lista dos repositórios coletados)*  
│  │  ├─ 📄 resultados_totais.csv *(Métricas extraídas dos repositórios)*  
│  │  ├─ 📄 matriz_correlacao.png *(Gráfico de correlação das métricas)*  
│  │  ├─ 📄 analise_metrica_ck.csv *(Resumo estatístico das métricas)*  
│  ├─ 📄 ck.jar *(Ferramenta CK para análise de código Java)*  
│  ├─ 🐍 coleta_repositorios.py *(Coleta repositórios via API GitHub)*  
│  ├─ 🐍 automacao_clone.py *(Clona os repositórios listados)*  
│  ├─ 🐍 coletar_dados.py *(Executa a ferramenta CK e coleta métricas)*  
│  ├─ 🐍 analisar_dados.py *(Processa e analisa os dados coletados)*  
│  ├─ 🐍 main.py *(Pipeline completo do laboratório)*  
│
├─ 📂 Lab2S02 *(Sprint 2: Relatório Final e Documentação)*  
│  ├─ 📂 Docs *(Relatórios e arquivos auxiliares)*  
│  │  ├─ 📜 relatório_final.txt *(Relatório final do laboratório)*  
│
├─ 📜 LABORATÓRIO_02.pdf *(Descrição da atividade)*  
├─ 📜 README_Lab2.md *(Instruções detalhadas do laboratório)*  
├─ 📜 .env.config *(Configuração do token GitHub e variáveis do projeto)*  
```

---

## 🔑 **Configuração do Token da API GitHub**  

O script de coleta requer um **token de autenticação** do GitHub. O token pode ser configurado automaticamente via terminal ou salvo em um arquivo `.env.config` na raiz do projeto, no seguinte formato:

```
GITHUB_TOKEN=seu_token_aqui
```

Caso precise gerar um token, siga os passos:  
1. Acesse [GitHub Developer Settings](https://github.com/settings/tokens).  
2. Clique em **"Generate new token (classic)"**.  
3. Selecione as permissões:  
   - `repo` → Acesso a repositórios públicos  
   - `read:org` → Acesso a informações organizacionais (se necessário)  
4. Copie o token gerado e adicione ao projeto.  

---

## 🚀 **Sprints do Projeto**  

### 📌 **Sprint 1 - Coleta de Dados e Análise Inicial**  

🔹 **Objetivos:**  
- Coletar **1000 repositórios Java** populares via **API do GitHub**.  
- Clonar os repositórios coletados automaticamente.  
- Extrair métricas de código usando a ferramenta **CK**.  
- Organizar e armazenar os dados coletados para análise.  

🔹 **Dependências:**  
```bash
pip install requests pandas python-dotenv gitpython matplotlib seaborn
```

### ▶️ **Como Executar**  

1️⃣ **Clone o repositório:**  
```bash
git clone https://github.com/RubbiaMattos/Lab_Experimentacao_Software_1.2025.git
cd Lab_Experimentacao_Software_1.2025/Lab2_QualiJava
```

2️⃣ **Execute todo o pipeline:**  
```bash
python main.py --step all
```

✅ Coleta dos repositórios via API  
✅ Clonagem dos repositórios listados  
✅ Coleta de métricas de qualidade do código  
✅ Análise inicial dos dados coletados  

---

### 📊 **Resultados da Sprint 1**  

📂 **Lab2S01/data/** gerou os seguintes arquivos:  
- **📂 ck_output/** → Métricas extraídas pelo CK (**class.csv, method.csv, field.csv, variable.csv**).  
- **📂 repos/** → Repositórios clonados para análise.  
- **📄 repositorios_list.csv** → Lista dos 1000 repositórios Java coletados.  
- **📄 resultados_totais.csv** → Consolidação das métricas extraídas.  
- **📄 matriz_correlacao.png** → Gráfico de correlação das métricas.  
- **📄 analise_metrica_ck.csv** → Estatísticas descritivas.  

🔹 **Principais Insights:**  
📌 Possível relação entre **tamanho do código (LOC)** e **acoplamento (CBO)**.  
📌 Projetos **mais antigos** tendem a apresentar **menor coesão (LCOM alto)**.  
📌 Repositórios **mais populares** podem ter código de **melhor qualidade**.  

🚀 *Próximos passos na Sprint 2: análise detalhada e geração de relatórios!*  

---

### 📌 **Sprint 2 - Planejamento e Próximos Passos**  

🔹 **Objetivos:**  
- Revisão e organização dos dados coletados.  
- Definição de hipóteses e padrões a serem analisados.  
- Aplicação de estatísticas e cálculos de correlação entre métricas.  
- Geração de gráficos e relatórios detalhados.  

🔹 **O que será feito?**  
1️⃣ **Revisão e limpeza dos dados** → Verificar inconsistências e outliers.  
2️⃣ **Definição de hipóteses** → Como maturidade, popularidade e qualidade do código se relacionam?  
3️⃣ **Geração de estatísticas e gráficos** → Correlações, distribuições e padrões.  
4️⃣ **Documentação dos resultados** → Criar um relatório consolidando insights.  

🔹 **Ferramentas e Bibliotecas:**  
- **Linguagem:** Python 3.8+  
- **Bibliotecas:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`  

---

## 📢 **Equipe do Projeto**  

👥 **Nataniel Geraldo Mendes Peixoto**  
👥 **Nelson de Campos Nolasco**  
👥 **Rubia Coelho de Matos**  
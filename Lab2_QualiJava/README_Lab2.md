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
├─ 📂 Lab2S01 *(Coleta e Análise Inicial)*
│  ├─ 🐍 coleta_repositorios.py
│  ├─ 🐍 automacao_clone.py
│  ├─ 🐍 coletar_dados.py
│  ├─ 🐍 analisar_dados.py
│  ├─ 🐍 main.py
│  ├─ 📄 ck.jar
│  ├─ 📂 Data
│  │  ├─ repositorios_list.csv
│  │  ├─ resultados_totais.csv
│  │  ├─ analise_metrica_ck.csv
│  │  ├─ 📂 ck_output_* *(Diretórios por repositório - saída do CK)*
│  ├─ 📂 Repos *(Repositórios clonados)*
│  ├─ 📂 Relatórios
│  │  ├─ clone_repositorios_log.log
│  │  ├─ coleta_repositorios_log.log
│  │  ├─ coletar_dados_log.log
│  │  ├─ correlacao_p_values_rq01.csv
│  │  ├─ correlacao_p_values_rq02.csv
│  │  ├─ correlacao_p_values_rq03.csv
│  │  ├─ correlacao_p_values_rq04.csv
│  │  ├─ boxplot_LOC.png
│  │  ├─ boxplot_LOC_log.png
│  │  ├─ histograma_CBO.png
│  │  ├─ histograma_DIT.png
│  │  ├─ histograma_LCOM.png
│  │  ├─ histograma_LOC.png
│  │  ├─ histograma_Comments.png
│  │  ├─ histograma_Maturity.png
│  │  ├─ histograma_Release.png
│  │  ├─ histograma_Stars.png
│  │  ├─ popularidade_qualidade_CBO.png
│  │  ├─ popularidade_qualidade_DIT.png
│  │  ├─ popularidade_qualidade_LCOM.png
│  │  ├─ maturidade_qualidade_CBO.png
│  │  ├─ maturidade_qualidade_DIT.png
│  │  ├─ maturidade_qualidade_LCOM.png
│  │  ├─ release_qualidade_CBO.png
│  │  ├─ release_qualidade_DIT.png
│  │  ├─ release_qualidade_LCOM.png
│  │  ├─ loc_qualidade_CBO.png
│  │  ├─ loc_qualidade_DIT.png
│  │  ├─ loc_qualidade_LCOM.png
│
├─ 📂 Lab2S02 *(Sprint 2 - Análises Finais e Relatório)*
│  ├─ 🐍 coleta_repositorios.py
│  ├─ 🐍 automacao_clone.py
│  ├─ 🐍 coletar_dados.py
│  ├─ 🐍 analisar_dados.py
│  ├─ 🐍 main.py
│  ├─ 📄 ck.jar
│  ├─ 📂 data
│  │  ├─ repositorios_list.csv
│  │  ├─ resultados_totais.csv
│  │  ├─ analise_metrica_ck.csv
│  ├─ 📂 Repos *(Repositórios clonados)*
│  ├─ 📂 Relatórios
│  │  ├─ Logs (clone, coleta, análise)
│  │  ├─ histogramas e boxplots
│  │  ├─ gráficos de correlação das 4 RQs
│  │  ├─ correlações (rq01 → rq04)
│  │  ├─ 📄 Análise de Repositórios Populares Java GitHub.docx
│  │  ├─ 📄 Análise de Repositórios Populares Java GitHub.pdf
│
├─ 📜 LABORATÓRIO_02.pdf
├─ 📜 README_Lab2.md
```

---

## 🔑 **Configuração do Token da API GitHub**  

O script de coleta requer um **token de autenticação** do GitHub. O token pode ser configurado automaticamente via terminal ou salvo em um arquivo `env.config` na raiz do projeto, no seguinte formato:

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

## 🚀 **Como Executar o Projeto (Completo ou Etapas Individuais)**

### 📦 **1. Instalar dependências**
```bash
pip install requests pandas python-dotenv gitpython matplotlib seaborn scipy numpy statsmodels tabulate tqdm
```

---

### ⚙ **2. Configurar o Token GitHub**
No arquivo:
```
Lab_Experimentacao_Software_1.2025\env.config
```
Exemplo:
```
GITHUB_TOKEN=seu_token_aqui
```

---

### ▶ **3. Executar o pipeline**
Dentro da pasta `Lab2S02`, rode o pipeline com:
```bash
python main.py --step all
```

O sistema:
✅ Pergunta se deseja limpar as pastas `Data/` e `Repos/`  
✅ Caso SIM, limpa as pastas  
✅ **Após limpar**, o pipeline **executa automaticamente todas as etapas** na sequência:
1. Buscar repositórios
2. Clonar repositórios
3. Rodar o CK
4. Analisar os dados e gerar os relatórios

---

### ✅ **4. Executar apenas a limpeza e escolher a etapa**
Se você quiser **limpar e rodar só uma parte**, execute direto com:
```bash
python main.py --step buscar      # Apenas busca os repositórios
python main.py --step clone       # Apenas clona os repositórios
python main.py --step coletar     # Apenas executa o CK e coleta dados
python main.py --step analisar    # Apenas analisa e gera os gráficos/relatórios
```
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

## 📌 **Sprint 2 - Análise Estatística, Gráficos e Relatório Final**

### 🔧 **Atividades Executadas**
✅ Recoleta e verificação dos repositórios  
✅ Reexecução da coleta de métricas CK  
✅ Geração de análises estatísticas e matrizes de correlação  
✅ Geração de histogramas, boxplots e gráficos das RQs  
✅ Aplicação dos testes estatísticos (Pearson e Spearman)  
✅ Geração do relatório final `.pdf` e `.docx`

---

## 🚀 **Como Executar o Projeto (Completo ou Etapas Individuais)**

### 📦 **1. Instalar dependências**
```bash
pip install requests pandas python-dotenv gitpython matplotlib seaborn scipy numpy statsmodels tabulate tqdm
```

---

### ⚙ **2. Configurar o Token GitHub**
No arquivo:
```
Lab_Experimentacao_Software_1.2025\env.config
```
Exemplo:
```
GITHUB_TOKEN=seu_token_aqui
```

---

### ▶ **3. Executar o pipeline**
Dentro da pasta `Lab2S02`, rode o pipeline com:
```bash
python main.py --step all
```

O sistema:
✅ Pergunta se deseja limpar as pastas `Data/` e `Repos/`  
✅ Caso SIM, limpa as pastas  
✅ **Após limpar**, o pipeline **executa automaticamente todas as etapas** na sequência:
1. Buscar repositórios
2. Clonar repositórios
3. Rodar o CK
4. Analisar os dados e gerar os relatórios

---

### 📊 **Saídas da Sprint 2**

#### 📂 **Lab2S02/data**
```
📄 repositorios_list.csv      -> Lista dos repositórios coletados
📄 resultados_totais.csv      -> Todas as métricas coletadas por repositório
📄 analise_metrica_ck.csv     -> Estatísticas descritivas das métricas
```

---

#### 📂 **Lab2S02/Relatórios**
```
📄 clone_repositorios_log.log
📄 coleta_repositorios_log.log
📄 coletar_dados_log.log
📄 analisar_dados_log.log

📄 correlacao_p_values_rq01.csv   -> Popularidade x Qualidade
📄 correlacao_p_values_rq02.csv   -> Maturidade x Qualidade
📄 correlacao_p_values_rq03.csv   -> Atividade x Qualidade
📄 correlacao_p_values_rq04.csv   -> Tamanho (LOC) x Qualidade

📊 boxplot_LOC.png

📊 Histogramas:
   - histograma_CBO.png
   - histograma_DIT.png
   - histograma_LCOM.png
   - histograma_LOC.png
   - histograma_Comments.png
   - histograma_Maturity.png
   - histograma_Release.png
   - histograma_Stars.png

📊 Gráficos de correlação:
   - popularidade_qualidade_CBO.png / DIT / LCOM
   - maturidade_qualidade_CBO.png / DIT / LCOM
   - release_qualidade_CBO.png / DIT / LCOM
   - loc_qualidade_CBO.png / DIT / LCOM

📄 Análise de Repositórios Populares Java GitHub.pdf (Relatório final)
📄 Análise de Repositórios Populares Java GitHub.docx
```

---

### 📜 **Resumo Estatístico da Sprint 2 (Extraído do PDF)**
✔ Total de repositórios analisados: **979**  
✔ Principais médias:
- **CBO**: 5 (baixo acoplamento)
- **DIT**: 4 (herança moderada)
- **LCOM**: 115 (baixa coesão com outliers)
- **LOC**: 180 mil linhas de código em média
- **Maturidade**: 9 anos
- **Releases**: 14 em média
- **Estrelas**: 9.281 (mín. 3.301 - máx. 148.824)

---

### 📈 **Resultados das RQs**
- **RQ1 (Popularidade)** → Popularidade está associada a menor CBO e DIT (menos acoplamento e herança).
- **RQ2 (Maturidade)** → Mais maturidade → maior DIT e menor coesão (LCOM).
- **RQ3 (Atividade - Releases)** → Mais releases aumentam CBO, DIT e impactam negativamente na coesão.
- **RQ4 (Tamanho - LOC)** → Repositórios grandes têm mais acoplamento, herança e menor coesão.

---

### ✅ **Entrega Final (Sprint 2)**
- Relatório **Análise de Repositórios Populares Java GitHub.pdf**
- CSVs de correlações
- Todos os gráficos e histogramas

---

🔹 **Ferramentas e Bibliotecas:**  
- **Linguagem:** Python 3.8+  
- **Bibliotecas:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`  

---

## 📢 **Equipe do Projeto**  

👥 **Nataniel Geraldo Mendes Peixoto**  
👥 **Nelson de Campos Nolasco**  
👥 **Rubia Coelho de Matos**  
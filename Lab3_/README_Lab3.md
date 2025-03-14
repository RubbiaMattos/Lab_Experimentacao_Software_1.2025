# 📌 **Laboratório 03 - Caracterizando a Atividade de Code Review no GitHub**

## 🎯 **Objetivo**

Este laboratório tem como objetivo **analisar a atividade de code review em repositórios populares do GitHub**, identificando variáveis que influenciam no merge de um Pull Request (PR).

---

## 🔎 **Questões de Pesquisa**

1. **Qual a relação entre o tamanho dos PRs e o feedback final das revisões?**  
2. **Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?**  
3. **Qual a relação entre a descrição dos PRs e o feedback final das revisões?**  
4. **Qual a relação entre as interações nos PRs e o feedback final das revisões?**  
5. **Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?**  
6. **Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?**  
7. **Qual a relação entre a descrição dos PRs e o número de revisões realizadas?**  
8. **Qual a relação entre as interações nos PRs e o número de revisões realizadas?**

---

## 📂 **Estrutura do Projeto** (Proposta)

```
📂 Lab3_Review
├─ 📂 Lab03S01 *(Sprint 1: Seleção de repositórios + Script de coleta de PRs)*
│  ├─ 🐍 coletar_repositorios.py *(coleta das URLs de 200 repositórios)*
│  ├─ 🐍 coletar_prs.py *(script que acessa a API e extrai métricas de PRs)*
│
├─ 📂 Lab03S02 *(Sprint 2: Dataset completo + Hipóteses iniciais)*
│  ├─ 📂 data *(CSV com PRs coletados, hipóteses em doc/txt)*
│
├─ 📂 Lab03S03 *(Sprint 3: Análise dos dados + Relatório final)*
│  ├─ 🐍 analisar_dados.py *(estatísticas, correlação)*
│  ├─ 📂 relatorio *(arquivos .pdf ou .docx com relatório final)*
│
├─ 📜 LABORATÓRIO_03.pdf *(Descrição da atividade)*
├─ 📜 README_Lab3.md *(Arquivo explicativo do laboratório)*
```

*(A nomenclatura e a estrutura de pastas podem ser ajustadas no decorrer do projeto.)*

---

## 🔧 Dependências (Provisórias)
- **Python 3.8+**
- `requests` (para acessar a API do GitHub)
- `pandas` (para manipular os dados dos PRs)
- `python-dotenv` (para gerenciar token do GitHub)
- `matplotlib` ou `seaborn` (visualização de dados)
- `scipy` ou `statsmodels` (testes de correlação)

---

## 🚀 Sprints do Projeto

### 📌 Sprint 1 - Coleta Inicial de Dados
**Tarefas**  
- Selecionar 200 repositórios populares no GitHub.  
- Criar scripts para coletar PRs (linhas adicionadas, removidas, tempo de revisão etc.).  
- Gerar um CSV inicial de teste (pull_requests_iniciais.csv).  

**Como Executar (Futuro)**  
1. Configurar `.env` com `GITHUB_TOKEN`.  
2. `python coletar_repositorios.py` para criar `repositorios_list.csv`.  
3. `python coletar_prs.py` para gerar `pull_requests_iniciais.csv`.

**Resultados Esperados**  
- Arquivos CSV iniciais contendo dados de alguns PRs.  
- Verificação se a coleta está funcionando.

**Status**  
❌ Ainda não iniciado

---

### 📌 Sprint 2 - Expansão do Dataset e Hipóteses Iniciais
**Tarefas**  
- Coletar PRs de todos os 200 repositórios.  
- Salvar métricas completas em `pull_requests_completo.csv`.  
- Elaborar hipóteses iniciais em `hipoteses_iniciais.md`.

**Como Executar (Futuro)**  
1. Reexecutar scripts para todos os repositórios.  
2. Verificar se `pull_requests_completo.csv` contém todas as colunas necessárias.  
3. Discutir e escrever hipóteses (ex.: “PRs maiores demoram mais para serem merged”).

**Resultados Esperados**  
- Dataset final com todos os PRs.  
- Documento com hipóteses e possíveis correlações.

**Status**  
❌ Ainda não iniciado

---

### 📌 Sprint 3 - Análise e Visualização de Dados
**Tarefas**  
- Aplicar estatística descritiva (média, mediana, desvio padrão).  
- Fazer testes de correlação (Spearman ou Pearson).  
- Criar gráficos e relatório final.

**Como Executar (Futuro)**  
1. `python analisar_dados.py` para gerar estatísticas e gráficos.  
2. Consolidar achados em `relatorio_final.pdf`.

**Resultados Esperados**  
- Gráficos mostrando relações entre tamanho, tempo, descrição e feedback.  
- Relatório final com conclusões.

**Status**  
❌ Ainda não iniciado

---

## 📝 Observações
- Nenhuma implementação foi feita ainda; tudo é **planejamento**.
- Cada sprint deverá atualizar este README com instruções e resultados concretos.
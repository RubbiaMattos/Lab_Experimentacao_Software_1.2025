# 📌 **Laboratório 05 - GraphQL vs REST - Um Experimento Controlado**

## 🎯 **Objetivo**

Este laboratório busca **avaliar quantitativamente os benefícios da adoção de GraphQL em comparação com REST** em APIs Web.

---

## 🔎 **Questões de Pesquisa**

1. **Consultas GraphQL são mais rápidas que consultas REST?**  
2. **As respostas GraphQL são menores que as respostas REST?**

---

## 📂 **Estrutura do Projeto** (Proposta)

```
📂 Lab5_Experiment
├─ 📂 Lab05S01 *(Sprint 1: Desenho e Preparação do Experimento)*
│  ├─ 🐍 design_experimento.md *(hipóteses, variáveis, etc.)*
│  ├─ 🐍 setup_ambiente.py *(scripts de teste, se necessário)*
│
├─ 📂 Lab05S02 *(Sprint 2: Execução e Análise dos Resultados)*
│  ├─ 📂 data *(coleta dos dados - CSVs com tempos de resposta e tamanhos)*
│  ├─ 🐍 analisar_resultados.py *(cálculos estatísticos)*
│
├─ 📂 Lab05S03 *(Sprint 3: Criação do Dashboard de Visualização)*
│  ├─ 📂 dashboard *(arquivos .pbix, .twb, ou gráficos em .png)*
│  ├─ 📂 relatorio *(relatório final consolidado)*
│
├─ 📜 LABORATÓRIO_05.pdf *(Descrição da atividade)*
├─ 📜 README_Lab5.md *(Arquivo explicativo do laboratório)*
```

---

## 🔑 **Dependências** (Possíveis)

- **Python 3.8+**
- `requests` (para enviar requisições REST e GraphQL)
- `pandas`, `numpy` (para manipulação dos dados coletados)
- `scipy` ou `statsmodels` (para testes estatísticos)
- Ferramenta de BI ou bibliotecas de visualização (`matplotlib`, `seaborn`) na Sprint 3

---

## 🚀 Sprints do Projeto

### 📌 Sprint 1 - Desenho e Preparação
**Tarefas**  
- Definir hipóteses (H0, H1) sobre tempo de resposta e tamanho.  
- Planejar número de medições, endpoints e amostras.  
- Preparar scripts de teste para REST e GraphQL.

**Como Executar (Futuro)**  
1. Criar endpoints de teste ou identificar APIs reais.  
2. Implementar `setup_ambiente.py` para configuração local.

**Resultados Esperados**  
- `design_experimento.md` detalhando hipóteses e variáveis.  
- Scripts básicos para rodar consultas.

**Status**  
❌ Ainda não iniciado

---

### 📌 Sprint 2 - Execução + Análise
**Tarefas**  
- Rodar experimentos, coletar dados (tempo, tamanho das respostas).  
- Analisar estatisticamente (média, mediana, desvio padrão, teste t, etc.).

**Como Executar (Futuro)**  
1. `python run_experimento.py` (exemplo) para gerar `resultados_experimento.csv`.  
2. `python analisar_resultados.py` para obter estatísticas e gráficos simples.

**Resultados Esperados**  
- `resultados_experimento.csv` com todas as medições.  
- Estatísticas iniciais comparando REST e GraphQL.

**Status**  
❌ Ainda não iniciado

---

### 📌 Sprint 3 - Dashboard + Relatório
**Tarefas**  
- Criar um dashboard (BI ou bibliotecas de visualização).  
- Redigir relatório final com conclusões e discussões.

**Como Executar (Futuro)**  
1. Importar `resultados_experimento.csv` na ferramenta escolhida.  
2. Gerar visualizações comparativas.  
3. Consolidar tudo em `relatorio_final.pdf`.

**Resultados Esperados**  
- Gráficos finais mostrando diferenças de performance.  
- Documento final com resposta às RQs (mais rápido? menor?).

**Status**  
❌ Ainda não iniciado

---

## 📝 Observações
- Nenhuma implementação foi iniciada.  
- As instruções são **planos** e podem mudar conforme o experimento for desenhado.

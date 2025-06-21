# 🧪 Laboratório 05 — GraphQL vs REST — Um Experimento Controlado

## 🎯 Objetivo

Este laboratório tem como objetivo avaliar quantitativamente as diferenças de desempenho entre chamadas REST e GraphQL à GitHub API, por meio de:

- **Medição de latência:** comparar o tempo médio de resposta (em segundos) de consultas equivalentes em ambas as APIs.  
- **Avaliação de payload:** comparar o tamanho médio (em bytes) dos dados retornados pelas mesmas consultas.  
- **Análise de consistência:** verificar a variabilidade das medições realizando múltiplas repetições e calculando desvio-padrão.  
- **Pareamento experimental:** garantir que as comparações sejam feitas sobre o mesmo conjunto de repositórios, controlando fatores externos.  

---

## 🗂️ Etapas do Projeto

1. **Desenho do Experimento**  
   - Definição de hipóteses (H0 e H1).  
   - Variáveis: **Tempo** (s), **Tamanho** (bytes) e **Tipo de API** (REST vs GraphQL).  
   - Documentação em `Desenho do Experimento.pdf`.  

2. **Implementação**  
   - `experiment.py`: executa 30 repetições de chamadas REST e GraphQL para cada repositório.  
   - Leitura de token GitHub via variável de ambiente `GITHUB_TOKEN`.  

3. **Coleta de Dados**  
   - Gera `experiment_results.csv` com colunas: `API_Type`, `Trial`, `Response_Time`, `Response_Size`.  

4. **Análise Estatística**  
   - `analysis.py`: agrega médias e desvios-padrão, produz `experiment_summary.csv`.  

5. **Visualização dos Resultados**  
   - `dashboard.py`: gera gráficos em `Gráficos/` (histograma de tempos e gráfico de barras de tamanho médio).  

6. **Documentação Final**  
   - Consolidação em `RelatorioFinal.docx`/`.pdf` e apresentação em PowerPoint.

---

## 🛠️ Como Executar

1. **Configurar token GitHub**  
```bash
   echo "GITHUB_TOKEN=seu_token_aqui" > .env
````

2. **Instalar dependências**

   ```bash
   pip install requests pandas matplotlib python-dotenv
   ```

3. **Pipeline completo**

   ```bash
   python experiment.py --owner <usuário> --repo <repositório> --trials 30
   python analysis.py
   python dashboard.py
   ```

---

## 📂 Saídas Esperadas

* `experiment_results.csv` — medições brutas de tempo e tamanho por trial
* `experiment_summary.csv` — estatísticas agregadas (média, desvio-padrão)
* Diretório `respostas_json/` — exemplos de payloads JSON (REST e GraphQL)
* Diretório `Gráficos/` —

  * `response_time_distribution.png`
  * `response_size_distribution.png`
* Diretório `Artefatos/` —

  * `RelatorioFinal.docx`
  * `RelatorioFinal.pdf`
  * `Apresentacao_Final.pptx`

---

## 🔎 Questões de Pesquisa (RQs)

| RQ   | Pergunta                                                                    |
| ---- | --------------------------------------------------------------------------- |
| RQ1  | Consultas GraphQL são mais rápidas que consultas REST?                      |
| RQ2  | As respostas GraphQL têm tamanho menor que as respostas REST?               |

---

## 📈 Métricas Utilizadas

| Categoria              | Métrica                                         |
| ---------------------- | ----------------------------------------------- |
| **Tempo de Resposta**  | Segundos entre requisição e chegada da resposta |
| **Tamanho de Payload** | Bytes do corpo da resposta                      |

---

## 👥 Equipe

* Nataniel Geraldo Mendes Peixoto
* Nelson de Campos Nolasco
* Rubia Coelho de Matos

---

## 📁 Estrutura do Projeto

```
Lab5_GraphXRest/
├── 📄 experiment.py                     # Script de execução do experimento
├── 📄 analysis.py                       # Gera estatísticas agregadas
├── 📄 dashboard.py                      # Cria histogramas e gráficos de barras
├── 📄 Desenho do Experimento.pdf        # Documento de desenho experimental
├── 📄 LABORATÓRIO_05.pdf                # Enunciado oficial do laboratório
├── 📄 README_Lab5.md                    # Documentação deste projeto

├── 📂 respostas_json/                   # Exemplos de payloads JSON
│   ├── graphql_response.json
│   └── rest_response.json

├── 📄 experiment_results.csv           # Dados brutos do experimento
├── 📄 experiment_summary.csv           # Estatísticas agregadas

├── 📂 Gráficos/                         # Visualizações geradas
│   ├── response_time_distribution.png
│   └── response_size_distribution.png

└── 📂 Artefatos/                        # Documentos finais
    ├── RelatorioFinal.docx
    ├── RelatorioFinal.pdf
    └── Apresentacao_Final.pptx
```
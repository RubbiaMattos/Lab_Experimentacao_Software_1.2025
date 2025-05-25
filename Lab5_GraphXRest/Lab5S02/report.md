# Relatório Final – GraphQL vs REST: GitHub API
# relatório em Markdown descrevendo experimento, resultados e conclusões
## 1. Introdução
Este experimento compara o desempenho de chamadas à **GitHub REST API** e à **GitHub GraphQL API**, medindo:
- **RQ1:** Qual API retorna dados mais rapidamente?
- **RQ2:** Qual API devolve payloads menores?

## 2. Desenho do Experimento
### A. Hipóteses
- **H0:** Não há diferença significativa entre REST e GraphQL (tempo e tamanho).
- **H1:** GraphQL é mais eficiente (menor tempo e tamanho).

### B. Variáveis
- **Dependentes:** Tempo de resposta (s), Tamanho do payload (bytes).  
- **Independente:** Tipo de API (_REST_ vs _GraphQL_).

### C. Endpoints
- **REST API:**  

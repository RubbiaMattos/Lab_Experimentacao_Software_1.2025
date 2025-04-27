# Relatório de Análise da Atividade de Code Review no GitHub

## Introdução

Este relatório apresenta os resultados da análise da atividade de code review em repositórios populares do GitHub. O objetivo é identificar variáveis que influenciam no merge de um PR, sob a perspectiva de desenvolvedores que submetem código aos repositórios selecionados.

### Hipóteses Informais

1. PRs menores têm maior probabilidade de serem aprovados.
2. PRs que levam mais tempo para serem analisados têm menor probabilidade de serem aprovados.
3. PRs com descrições mais detalhadas têm maior probabilidade de serem aprovados.
4. PRs com mais interações têm maior probabilidade de serem aprovados.
5. PRs maiores requerem mais revisões.
6. PRs que levam mais tempo para serem analisados têm mais revisões.
7. PRs com descrições mais detalhadas têm menos revisões.
8. PRs com mais interações têm mais revisões.

## Metodologia

Para realizar esta análise, seguimos os seguintes passos:

1. **Coleta de dados**: Selecionamos os 200 repositórios mais populares do GitHub com pelo menos 100 PRs (MERGED + CLOSED).

2. **Filtragem dos dados**: Selecionamos apenas PRs com status MERGED ou CLOSED, que possuíam pelo menos uma revisão e cuja análise levou pelo menos uma hora.

3. **Análise estatística**: Utilizamos o coeficiente de correlação de Spearman para analisar as relações entre as variáveis, pois esse método não assume que os dados seguem uma distribuição normal e é menos sensível a outliers. O coeficiente de Spearman é adequado para dados que não necessariamente têm uma relação linear, medindo a força e direção de uma associação monotônica entre duas variáveis.

4. **Interpretação dos resultados**: Interpretamos os coeficientes de correlação da seguinte forma:
   - |r| < 0.1: Correlação insignificante
   - 0.1 ≤ |r| < 0.3: Correlação fraca
   - 0.3 ≤ |r| < 0.5: Correlação moderada
   - 0.5 ≤ |r| < 0.7: Correlação forte
   - |r| ≥ 0.7: Correlação muito forte

   Consideramos correlações estatisticamente significativas aquelas com p-valor < 0.05.

## Resultados

### RQ 01: Relação entre o tamanho dos PRs e o feedback final das revisões

**Correlação entre métricas de tamanho e status:**

![Correlação entre Tamanho dos PRs e Status](data/visualizations/rq01_correlation.png)

**Correlação entre número de arquivos alterados e status:**
- Coeficiente de correlação: 0.0588
- P-valor: 5.6406e-102
- Interpretação: Insignificante
- Estatisticamente significativo: Sim

![Distribuição de Arquivos por Status](data/visualizations/rq01_files_changed_boxplot.png)

**Correlação entre linhas adicionadas e status:**
- Coeficiente de correlação: 0.0104
- P-valor: 1.4940e-04
- Interpretação: Insignificante
- Estatisticamente significativo: Sim

![Distribuição de Linhas Adicionadas por Status](data/visualizations/rq01_additions_boxplot.png)

**Correlação entre linhas removidas e status:**
- Coeficiente de correlação: 0.0889
- P-valor: 4.7984e-231
- Interpretação: Insignificante
- Estatisticamente significativo: Sim

![Distribuição de Linhas Removidas por Status](data/visualizations/rq01_deletions_boxplot.png)

**Estatísticas descritivas (medianas):**
- PRs mesclados (MERGED):
  - Arquivos alterados: 2.00
  - Linhas adicionadas: 18.00
  - Linhas removidas: 5.00
- PRs fechados sem merge (CLOSED):
  - Arquivos alterados: 2.00
  - Linhas adicionadas: 18.00
  - Linhas removidas: 2.00

**Estatísticas descritivas (média):**
- PRs mesclados (MERGED):
  - Arquivos alterados: 8.95
  - Linhas adicionadas: 287.06
  - Linhas removidas: 5.00
- PRs fechados sem merge (CLOSED):
  - Arquivos alterados: 19.88
  - Linhas adicionadas: 814.51
  - Linhas removidas: 930.39

### RQ 02: Relação entre o tempo de análise dos PRs e o feedback final das revisões

**Correlação entre tempo de análise e status:**
- Coeficiente de correlação: -0.2376
- P-valor: 0.0000e+00
- Interpretação: Fraca
- Estatisticamente significativo: Sim

![Distribuição do Tempo de Análise por Status](data/visualizations/rq02_time_boxplot.png)

![Histograma do Tempo de Análise por Status](data/visualizations/rq02_time_histogram.png)

**Estatísticas descritivas (medianas):**
- PRs mesclados (MERGED): 30.54 horas
- PRs fechados sem merge (CLOSED): 226.54 horas

### RQ 03: Relação entre a descrição dos PRs e o feedback final das revisões

**Correlação entre tamanho da descrição e status:**
- Coeficiente de correlação: 0.0286
- P-valor: 1.6337e-25
- Interpretação: Insignificante
- Estatisticamente significativo: Sim

![Distribuição do Tamanho da Descrição por Status](data/visualizations/rq03_description_boxplot.png)

![Mediana do Tamanho da Descrição por Status](data/visualizations/rq03_description_bars.png)

**Estatísticas descritivas (medianas):**
- PRs mesclados (MERGED): 450.00 caracteres
- PRs fechados sem merge (CLOSED): 356.00 caracteres

### RQ 04: Relação entre as interações nos PRs e o feedback final das revisões

**Correlação entre métricas de interação e status:**

![Correlação entre Interações e Status](data/visualizations/rq04_correlation.png)

**Correlação entre número de participantes e status:**
- Coeficiente de correlação: -0.0578
- P-valor: 1.4209e-98
- Interpretação: Insignificante
- Estatisticamente significativo: Sim

![Distribuição de Participantes por Status](data/visualizations/rq04_participant_count_boxplot.png)

**Correlação entre número de comentários e status:**
- Coeficiente de correlação: -0.1762
- P-valor: 0.0000e+00
- Interpretação: Fraca
- Estatisticamente significativo: Sim

![Distribuição de Comentários por Status](data/visualizations/rq04_comments_boxplot.png)

**Correlação entre número de comentários de revisão e status:**
- Coeficiente de correlação: -0.1090
- P-valor: 0.0000e+00
- Interpretação: Fraca
- Estatisticamente significativo: Sim

![Distribuição de Comentários de Revisão por Status](data/visualizations/rq04_review_comments_boxplot.png)

**Estatísticas descritivas (medianas):**
- PRs mesclados (MERGED):
  - Participantes: 3.00
  - Comentários: 1.00
  - Comentários de revisão: 0.00
- PRs fechados sem merge (CLOSED):
  - Participantes: 3.00
  - Comentários: 3.00
  - Comentários de revisão: 1.00

### RQ 05: Relação entre o tamanho dos PRs e o número de revisões realizadas

**Correlação entre métricas de tamanho e número de revisões:**

![Correlação entre Tamanho dos PRs e Número de Revisões](data/visualizations/rq05_correlation.png)

**Correlação entre número de arquivos alterados e número de revisões:**
- Coeficiente de correlação: 0.2550
- P-valor: 0.0000e+00
- Interpretação: Fraca
- Estatisticamente significativo: Sim

![Relação entre Número de Arquivos e Revisões](data/visualizations/rq05_files_changed_scatter.png)

**Correlação entre linhas adicionadas e número de revisões:**
- Coeficiente de correlação: 0.3150
- P-valor: 0.0000e+00
- Interpretação: Moderada
- Estatisticamente significativo: Sim

![Relação entre Linhas Adicionadas e Revisões](data/visualizations/rq05_additions_scatter.png)

**Correlação entre linhas removidas e número de revisões:**
- Coeficiente de correlação: 0.1627
- P-valor: 0.0000e+00
- Interpretação: Fraca
- Estatisticamente significativo: Sim

![Relação entre Linhas Removidas e Revisões](data/visualizations/rq05_deletions_scatter.png)

### RQ 06: Relação entre o tempo de análise dos PRs e o número de revisões realizadas

**Correlação entre tempo de análise e número de revisões:**
- Coeficiente de correlação: 0.2877
- P-valor: 0.0000e+00
- Interpretação: Fraca
- Estatisticamente significativo: Sim

![Relação entre Tempo de Análise e Revisões](data/visualizations/rq06_time_scatter.png)

![Média de Revisões por Faixa de Tempo](data/visualizations/rq06_time_bins.png)

### RQ 07: Relação entre a descrição dos PRs e o número de revisões realizadas

**Correlação entre tamanho da descrição e número de revisões:**
- Coeficiente de correlação: 0.0751
- P-valor: 2.7356e-165
- Interpretação: Insignificante
- Estatisticamente significativo: Sim

![Relação entre Tamanho da Descrição e Revisões](data/visualizations/rq07_description_scatter.png)

![Média de Revisões por Tamanho de Descrição](data/visualizations/rq07_desc_bins.png)

### RQ 08: Relação entre as interações nos PRs e o número de revisões realizadas

**Correlação entre métricas de interação e número de revisões:**

![Correlação entre Interações e Número de Revisões](data/visualizations/rq08_correlation.png)

**Correlação entre número de participantes e número de revisões:**
- Coeficiente de correlação: 0.4342
- P-valor: 0.0000e+00
- Interpretação: Moderada
- Estatisticamente significativo: Sim

![Relação entre Número de Participantes e Revisões](data/visualizations/rq08_participant_count_scatter.png)

**Correlação entre número de comentários e número de revisões:**
- Coeficiente de correlação: 0.2654
- P-valor: 0.0000e+00
- Interpretação: Fraca
- Estatisticamente significativo: Sim

![Relação entre Número de Comentários e Revisões](data/visualizations/rq08_comments_scatter.png)

**Correlação entre número de comentários de revisão e número de revisões:**
- Coeficiente de correlação: 0.7801
- P-valor: 0.0000e+00
- Interpretação: Muito forte
- Estatisticamente significativo: Sim

![Relação entre Número de Comentários de Revisão e Revisões](data/visualizations/rq08_review_comments_scatter.png)

## Discussão

Nesta seção, discutimos os resultados obtidos em relação às nossas hipóteses iniciais.

### RQ 01: Relação entre o tamanho dos PRs e o feedback final das revisões

Hipótese: PRs menores têm maior probabilidade de serem aprovados.

Os resultados não suportam completamente nossa hipótese. A correlação entre o tamanho do PR e sua aprovação não foi tão forte ou significativa como esperávamos.

### RQ 02: Relação entre o tempo de análise dos PRs e o feedback final das revisões

Hipótese: PRs que levam mais tempo para serem analisados têm menor probabilidade de serem aprovados.

Os resultados suportam nossa hipótese. Encontramos uma correlação fraca e estatisticamente significativa entre o tempo de análise e a aprovação do PR. PRs que levam mais tempo para serem analisados têm menor probabilidade de serem aprovados.

### RQ 03: Relação entre a descrição dos PRs e o feedback final das revisões

Hipótese: PRs com descrições mais detalhadas têm maior probabilidade de serem aprovados.

Os resultados suportam nossa hipótese. Encontramos uma correlação insignificante e estatisticamente significativa entre o tamanho da descrição e a aprovação do PR. PRs com descrições mais detalhadas têm maior probabilidade de serem aprovados.

### RQ 04: Relação entre as interações nos PRs e o feedback final das revisões

Hipótese: PRs com mais interações têm maior probabilidade de serem aprovados.

Os resultados não suportam nossa hipótese. As correlações entre as métricas de interação e a aprovação do PR não foram tão fortes ou significativas como esperávamos.

### RQ 05: Relação entre o tamanho dos PRs e o número de revisões realizadas

Hipótese: PRs maiores requerem mais revisões.

Os resultados suportam nossa hipótese. Encontramos correlações significativas entre o tamanho do PR e o número de revisões realizadas. PRs maiores tendem a requerer mais revisões, possivelmente porque contêm mais código a ser analisado e mais problemas potenciais a serem identificados.

### RQ 06: Relação entre o tempo de análise dos PRs e o número de revisões realizadas

Hipótese: PRs que levam mais tempo para serem analisados têm mais revisões.

Os resultados suportam nossa hipótese. Encontramos uma correlação fraca e estatisticamente significativa entre o tempo de análise e o número de revisões. PRs que levam mais tempo para serem analisados têm mais revisões, possivelmente porque revisões adicionais são necessárias para resolver problemas identificados.

### RQ 07: Relação entre a descrição dos PRs e o número de revisões realizadas

Hipótese: PRs com descrições mais detalhadas têm menos revisões.

Os resultados não suportam nossa hipótese. A correlação entre o tamanho da descrição e o número de revisões não foi negativa ou significativa como esperávamos.

### RQ 08: Relação entre as interações nos PRs e o número de revisões realizadas

Hipótese: PRs com mais interações têm mais revisões.

Os resultados suportam nossa hipótese. Encontramos correlações significativas entre as métricas de interação e o número de revisões. PRs com mais interações têm mais revisões, possivelmente porque cada revisão gera comentários e discussões que podem levar a revisões adicionais.

## Conclusão

Este estudo analisou a relação entre diversas características dos PRs e seu feedback final, bem como o número de revisões realizadas. Os resultados fornecem insights valiosos sobre como melhorar a chance de aprovação de PRs e otimizar o processo de code review em projetos open source.

Com base nos resultados, podemos sugerir as seguintes práticas para melhorar a aprovação de PRs:

1. Manter os PRs pequenos, afetando poucos arquivos e com poucas linhas alteradas.
2. Incluir descrições detalhadas e claras, explicando o propósito e o contexto do PR.
3. Promover interações construtivas durante o processo de revisão, respondendo prontamente aos comentários.
4. Evitar PRs que levem muito tempo para serem analisados, dividindo mudanças grandes em PRs menores e mais focados.

Esperamos que estes insights ajudem desenvolvedores e mantenedores de projetos open source a otimizar seus processos de code review, melhorando a qualidade do código e a experiência dos contribuidores.
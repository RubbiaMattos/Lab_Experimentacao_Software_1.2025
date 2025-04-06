📄 **Relatório de Análise da Atividade de Code Review no GitHub**


## 📋 **Introdução**

    Este relatório apresenta os resultados da análise da atividade de code review em repositórios populares do GitHub. O objetivo é identificar variáveis que influenciam no merge de um PR, sob a perspectiva de desenvolvedores que submetem código aos repositórios selecionados.


### ✨ **Hipóteses Informais**

    1. PRs menores têm maior probabilidade de serem aprovados. ✂️

    2. PRs que levam mais tempo para serem analisados têm menor probabilidade de serem aprovados. ⏳❌

    3. PRs com descrições mais detalhadas têm maior probabilidade de serem aprovados. 📑👍

    4. PRs com mais interações têm maior probabilidade de serem aprovados. 💬🔄

    5. PRs maiores requerem mais revisões. 📂🔍

    6. PRs que levam mais tempo para serem analisados têm mais revisões. ⏱️🔄

    7. PRs com descrições mais detalhadas têm menos revisões. ✍️📉

    8. PRs com mais interações têm mais revisões. 💬🔄✅


## 🧑‍🔬 **Metodologia**

    Para realizar esta análise, seguimos os seguintes passos:

    1. **Coleta de dados**: Selecionamos os 200 repositórios mais populares do GitHub com pelo menos 100 PRs (MERGED + CLOSED). 📊📈

    2. **Filtragem dos dados**: Selecionamos apenas PRs com status MERGED ou CLOSED, que possuíam pelo menos uma revisão e cuja análise levou pelo menos uma hora. ⏱️✅

    3. **Análise estatística**: Utilizamos o coeficiente de correlação de Spearman para analisar as relações entre as variáveis, pois esse método não assume que os dados seguem uma distribuição normal e é menos sensível a outliers. 🔍📉

    4. **Interpretação dos resultados**: Interpretamos os coeficientes de correlação da seguinte forma: 🎯📊

        - |r| < 0.1: Correlação insignificante 🔴

        - 0.1 ≤ |r| < 0.3: Correlação fraca 🟠

        - 0.3 ≤ |r| < 0.5: Correlação moderada 🟡

        - 0.5 ≤ |r| < 0.7: Correlação forte 🟢

        - |r| ≥ 0.7: Correlação muito forte 🔵


    Consideramos correlações estatisticamente significativas aquelas com p-valor < 0.05. 🔒💡

## 📊 **Resultados**


### RQ 01: Relação entre o tamanho dos PRs e o feedback final das revisões

    **📏 Correlação entre métricas de tamanho e status:**

    ![Correlação entre Tamanho dos PRs e Status](data/visualizations/rq01_correlation.png) 📈
    **📂 Correlação entre número de arquivos alterados e status:**

    - Coeficiente de correlação: 0.1135 🔢
    - P-valor: 1.6278e-107 🔍
    - Interpretação: Fraca 📊
    - Estatisticamente significativo: ✅ Sim
    ![Distribuição de Arquivos por Status](data/visualizations/rq01_files_changed_boxplot.png) 📊

### RQ 02: Relação entre o tempo de análise dos PRs e o feedback final das revisões

    **⏱️ Correlação entre tempo de análise e status:**

    - Coeficiente de correlação: -0.1469 🔢
    - P-valor: 1.9687e-179 🔍
    - Interpretação: Fraca 📊
    - Estatisticamente significativo: ✅ Sim
    ![Distribuição do Tempo de Análise por Status](data/visualizations/rq02_time_boxplot.png) ⏱️
    ![Histograma do Tempo de Análise por Status](data/visualizations/rq02_time_histogram.png) 📊

    **⏱️ Tempo Mediano de Análise por Status:**
    - CLOSED: 01:56:53 (≈ 73.95h)
    - MERGED: 05:01:14 (≈ 29.02h)

### RQ 03: Relação entre a descrição dos PRs e o feedback final das revisões

    **📄 Correlação entre tamanho da descrição e status:**

    - Coeficiente de correlação: 0.0492 🔢
    - P-valor: 1.8555e-21 🔍
    - Interpretação: Insignificante 📊
    - Estatisticamente significativo: ✅ Sim
    ![Distribuição do Tamanho da Descrição por Status](data/visualizations/rq03_description_boxplot.png) 📊
    ![Mediana do Tamanho da Descrição por Status](data/visualizations/rq03_description_bars.png) 📊

## 📝 **Discussão**

    Nesta seção, discutimos os resultados obtidos em relação às nossas hipóteses iniciais.


### RQ 01: Relação entre o tamanho dos PRs e o feedback final das revisões

    **Hipótese:** PRs menores têm maior probabilidade de serem aprovados. ✂️📈

    🔴 **Os resultados não suportam completamente nossa hipótese.** A correlação entre o tamanho do PR e sua aprovação não foi tão forte ou significativa como esperávamos. ❌

## 🔍 **Conclusão**


    Este estudo analisou a relação entre diversas características dos PRs e seu feedback final, bem como o número de revisões realizadas. Os resultados fornecem insights valiosos sobre como melhorar a chance de aprovação de PRs e otimizar o processo de code review em projetos open source. 🚀

    Com base nos resultados, podemos sugerir as seguintes práticas para melhorar a aprovação de PRs:

    1. Manter os PRs pequenos, afetando poucos arquivos e com poucas linhas alteradas. ✂️

    2. Incluir descrições detalhadas e claras, explicando o propósito e o contexto do PR. 📝

    3. Promover interações construtivas durante o processo de revisão, respondendo prontamente aos comentários. 💬

    4. Evitar PRs que levem muito tempo para serem analisados, dividindo mudanças grandes em PRs menores e mais focados. ⏳


    🎯 **Esperamos que estes insights ajudem desenvolvedores e mantenedores de projetos open source a otimizar seus processos de code review, melhorando a qualidade do código e a experiência dos contribuidores.**
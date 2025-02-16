# 📊 LaboratórioExperimentação de Software

Este repositório contém uma série de laboratórios conduzidos na disciplina **Laboratório de Experimentação de Software** do curso de **Engenharia de Software**, ministrado pelo professor **João Paulo Carneiro Aramuni**. Os laboratórios exploram características e boas práticas no desenvolvimento de software, especialmente no contexto de projetos open-source e tecnologias emergentes.

---

## 📌 Lista de Laboratórios

### 🔹 [Laboratório 01 - Características de Repositórios Populares](Documentos/LABORATÓRIO_01.pdf) 

📌 **Objetivo:** 
Estudar as principais características dos repositórios mais populares no GitHub, analisando fatores como idade, contribuições externas, frequência de releases e linguagens utilizadas.

📂 **Principais Análises:**
- Relação entre idade e popularidade dos repositórios.
- Impacto das contribuições externas (Pull Requests aceitos) na evolução dos projetos.
- Frequência de lançamento de releases e estabilidade do repositório.
- Principais linguagens de programação utilizadas.
- Percentual de issues fechadas como indicador de manutenção ativa.
- Comparação entre linguagens populares e sua relação com contribuições externas, releases e atualizações frequentes (RQ 07 - Bônus).

⚙️ **Implementação - Lab01S01:**
- Desenvolvimento de uma consulta **GraphQL** para coletar dados de **100 repositórios** mais populares do GitHub.
- Coleta de métricas essenciais, incluindo:
  - **Idade do repositório** (data de criação).
  - **Total de Pull Requests aceitos**.
  - **Número total de releases**.
  - **Data da última atualização**.
  - **Linguagem primária do repositório**.
  - **Percentual de issues fechadas**.
- Armazenamento dos dados coletados em um **arquivo CSV**.
- Implementação de um **sistema de requisição automática** para recuperar os dados necessários sem o uso de bibliotecas externas que realizem chamadas à API do GitHub.
- Estruturação do código em **RepoPop100.py**, garantindo modularidade e eficiência na obtenção das informações.

📂 **Estrutura do Diretório:**
```
📂 Lab1_RepoPop
 ├── 📂 Lab01S01
 │   ├── 📜 .env.config
 │   ├── 📂 Relatórios
 │   │   ├── 📄 Análise de Repositórios Populares no GitHub.docx
 │   │   ├── 📄 Análise de Repositórios Populares no GitHub.pdf
 │   │   ├── 📊 github_analysis.csv
 │   │   ├── 📊 qtd_PRs_aceitos.png
 │   │   ├── 📊 top_languages.png
 │   ├── 🐍 RepoPop100.py
 ├── 📂 Lab01S02
 ├── 📂 Lab01S03
```

📌 **Como Executar a Lab01S01:**
```sh
git clone https://github.com/RubbiaMattos/Lab_Experimentacao_Software_1.2025.git
cd Lab_Experimentacao_Software_1.2025
cd Lab1_RepoPop/Lab01S01
```

🔑 **Configuração da Autenticação:**
O arquivo `.env.config` já está presente na pasta `Lab1_RepoPop/Lab01S01`. Para utilizá-lo, apenas edite e substitua o token existente por um válido:
```env
GITHUB_TOKEN=seu_novo_token_aqui
```

📦 **Instale as Dependências:**
```sh
py -3.12 -m pip install pandas requests matplotlib seaborn python-dotenv
```

▶️ **Execute o Script:**
```sh
python RepoPop100.py
```

📊 **Analise os Resultados:**
Os arquivos gerados, como gráficos e relatórios CSV, estarão disponíveis na pasta `Relatórios`. Para visualizar, utilize ferramentas como Excel, Google Sheets ou bibliotecas Python de análise de dados.

---

### 🔹 [Laboratório 02 - Qualidade de Sistemas Java](Documentos/LABORATÓRIO_02.pdf)

📌 **Objetivo:** Avaliar a qualidade do código em projetos Java, utilizando métricas como acoplamento, coesão e complexidade, e entender sua relação com a manutenibilidade do software.

📂 **Principais Análises:**
- Medição do acoplamento entre classes utilizando CBO (Coupling Between Objects).
- Avaliação da herança por meio da métrica DIT (Depth of Inheritance Tree).
- Análise da coesão entre métodos por meio do LCOM (Lack of Cohesion of Methods).
- Correlação entre popularidade do repositório e qualidade do código.
- Influência da frequência de commits e releases na legibilidade e modularidade do código.

### 🔹 [Laboratório 03 - Code Review no GitHub](Documentos/LABORATÓRIO_03.pdf)

📌 **Objetivo:** Investigar o papel do code review no processo de desenvolvimento colaborativo no GitHub, analisando métricas de engajamento e padrões de revisão.

📂 **Principais Análises:**
- Relação entre tamanho do Pull Request (PR) e sua taxa de aprovação ou rejeição.
- Tempo médio de revisão e sua influência na qualidade do feedback.
- Impacto da quantidade de revisores e interações nos PRs na sua aceitação.
- Comparação entre repositórios populares e menos conhecidos quanto às práticas de revisão de código.
- Papel das descrições detalhadas nos PRs na facilitação do processo de code review.

### 🔹 [Laboratório 04 - Visualização de Dados com BI](Documentos/LABORATÓRIO_04.pdf)

📌 **Objetivo:** Explorar o uso de ferramentas de Business Intelligence (BI) para transformar dados complexos em visualizações interativas e acessíveis.

📂 **Principais Análises:**
- Construção de dashboards dinâmicos para análise de dados experimentais.
- Utilização de ferramentas como Power BI, Tableau e Google Data Studio.
- Comparação de diferentes formas de visualização para otimizar a interpretação dos dados.
- Aplicação de técnicas de sumarização e filtragem para extrair insights relevantes.
- Demonstração de como a visualização de dados pode auxiliar na tomada de decisões em engenharia de software.

### 🔹 [Laboratório 05 - GraphQL vs REST](Documentos/LABORATÓRIO_05.pdf)

📌 **Objetivo:** Realizar um experimento controlado comparando GraphQL e REST em termos de desempenho, eficiência no consumo de dados e complexidade de implementação.

📂 **Principais Análises:**
- Tempo de resposta de requisições GraphQL vs REST em diferentes cenários.
- Comparação do tamanho dos dados trafegados e análise de overfetching/underfetching.
- Eficiência no consumo de dados em aplicações que utilizam GraphQL.
- Estudo de casos reais de migração de REST para GraphQL e seus impactos.
- Implementação de um experimento prático para medir as vantagens e desvantagens de cada abordagem.

---

## 🛠️ Tecnologias Utilizadas
- Python 3.12 (linguagem principal utilizada)
- Git e GitHub (controle de versão e repositório)
- GraphQL (tecnologia para consultas otimizadas na API do GitHub)

---

## 🛠️ Bibliotecas Externas
- Pandas (manipulação e análise de dados)
- Matplotlib & Seaborn (visualização de dados)
- Requests (requisições HTTP para API do GitHub)
- Dotenv (gerenciamento de variáveis de ambiente)
- Jupyter Notebook (ambiente interativo para análise de dados)

---

## 📖 Referências
- [Documentação do GitHub](https://docs.github.com/pt)
- [Octoverse - GitHub Insights](https://octoverse.github.com/)
- [GraphQL vs REST](https://graphql.org/learn/)

---

## 👥 Equipe
- **Nataniel Geraldo Mendes Peixoto**  
- **Nelson de Campos Nolasco**  
- **Rúbia Coelho de Matos**  

📌 **Professor:** João Paulo Carneiro Aramuni  
📌 **Curso:** Engenharia de Software  
📌 **Disciplina:** Laboratório de Experimentação de Software  
📌 **Instituição:** Pontifícia Universidade Católica de Minas Gerais (PUC Minas)

---


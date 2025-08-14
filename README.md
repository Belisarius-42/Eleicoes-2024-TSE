# 🗳️ Dashboard de Análise Eleitoral - Eleições 2024

![Status](https://img.shields.io/badge/status-concluído-green)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-red?logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-blue?logo=pandas)

**Dashboard interativo para análise de dados eleitorais, focado em explorar o perfil de candidatos, a composição de partidos e os resultados das eleições.**

### 🚀Acesse o Dashboard Online Aqui:
https://eleicoes2024-tse.streamlit.app/
https://eleicoes2024-tse.streamlit.app/
https://eleicoes2024-tse.streamlit.app/

---

## 🎯 Objetivo do Projeto

Este projeto tem como objetivo analisar os dados públicos de candidaturas disponibilizados pelo TSE (Tribunal Superior Eleitoral) para extrair insights sobre o cenário político. O dashboard interativo permite que o usuário explore:

* **Perfis demográficos:** Análise de gênero, raça/cor e escolaridade entre os candidatos.
* **Análise partidária:** Comparação da composição e do desempenho dos partidos e espectros ideológicos.
* **Patrimônio:** Investigação sobre os bens declarados pelos candidatos, utilizando a **mediana** como métrica principal para uma análise mais robusta contra valores extremos.
* **Análise Interseccional:** Um gráfico de dispersão que cruza as representatividades de gênero e raça, revelando padrões de diversidade nos partidos.

## ✨ Principais Análises e Funcionalidades

* **Visão Geral e Métricas:** KPIs (Key Performance Indicators) que resumem os dados, como taxa de sucesso eleitoral, contagem de candidatos e representatividade média.
* **Composição de Gênero, Raça e Escolaridade:** Gráficos de barras que detalham o perfil dos candidatos por partido e por espectro ideológico.
* **Ranking de Partidos:** Visualização dos 10 partidos com maior número absoluto de eleitos.
* **Análise de Patrimônio:** Comparação da mediana de bens declarados e histograma interativo para investigar a distribuição de riqueza em cada partido.
* **Filtros Interativos:** Seletores que permitem ao usuário "mergulhar" nos dados de um partido específico ou filtrar visualizações complexas.

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído utilizando um ecossistema de ferramentas de dados em Python. Cada tecnologia teve um papel crucial:
* **Python:** Linguagem principal para toda a lógica de manipulação de dados e construção do backend do aplicativo.
* **Streamlit:** Utilizado para construir e implantar a interface web interativa do dashboard de forma rápida e eficiente. Todos os componentes visuais, como gráficos, seletores e métricas, são renderizados com Streamlit.
* **Pandas:** A principal ferramenta para a limpeza, transformação, agregação e análise dos dados em memória. Após a carga inicial do banco de dados, todas as métricas e tabelas personalizadas para os gráficos foram geradas com `groupby`, `agg`, `merge` e outras funções do Pandas.
* **Plotly Express:** Responsável pela criação de todos os gráficos interativos do projeto (barras, pizza, dispersão e histograma), permitindo visualizações ricas com tooltips, zoom e filtros.
* **SQLAlchemy:** Utilizado para estabelecer a conexão com o banco de dados SQLite e executar a query principal que carrega os dados para o ambiente Python.
* **SQL (SQLite):** A linguagem usada no arquivo `query1.sql` para realizar a junção inicial das tabelas de candidaturas, bens e cassações. Esta etapa de pré-processamento no SQL foi fundamental para consolidar os dados em uma única tabela base.
* **Git & GitHub:** Para versionamento do código, controle das alterações e como plataforma para hospedar o código-fonte do projeto.
* **Streamlit Community Cloud:** Plataforma de nuvem utilizada para a hospedagem e disponibilização pública do dashboard, com integração contínua a partir do repositório no GitHub.

## 🗂️ O Fluxo de Dados

O projeto segue um pipeline de dados claro, desde a origem até a visualização:
1.  **Dados Brutos:** Os dados foram originados de arquivos CSV públicos do TSE.
2.  **Processamento (ETL):** Um script local (`ingestao.py`) foi usado para ler os CSVs, tratá-los e carregá-los em um banco de dados **SQLite (`database.db`)**. Esta etapa otimiza as consultas futuras.
3.  **Consulta Principal:** O arquivo `query1.sql` é executado na inicialização do app. Ele realiza os `JOIN`s mais importantes (bens, ideologia, cassação) e entrega uma única tabela limpa para o Streamlit.
4.  **Análise e Visualização:** O script `tse.py` carrega esses dados em um DataFrame Pandas e realiza todas as agregações e cálculos necessários para alimentar os gráficos interativos do Plotly.


## ✍️ Bruno Henrique

* **[SEU NOME AQUI]**
* **LinkedIn:** [SEU LINKEDIN AQUI]
* **GitHub:** [SEU GITHUB AQUI]

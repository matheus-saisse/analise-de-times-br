# Análise de Times BR — Campeonato Brasileiro (2003–2025)

Projeto de portfólio de análise de dados esportivos, com foco na evolução dos clubes do Rio de Janeiro no Campeonato Brasileiro, destacando o **Flamengo**. Pipeline completo: limpeza de dados em Python, modelagem relacional em SQL Server, e dashboard interativo em Power BI.

## Objetivo

Analisar com dados, como o Flamengo evoluiu ao longo de 22 temporadas do Brasileirão, comparado com os 4 grandes clubes do Rio de Janeiro.

## Pipeline do projeto

| Etapa | Ferramenta | Relatório |
|---|---|---|
| 1. Limpeza e tratamento dos dados | Python, Pandas, Numpy | [`docs/RELATORIO_LIMPEZA_DADOS.md`](docs/RELATORIO_LIMPEZA_DADOS.md) |
| 2. Importação para o banco relacional | SQL Server | [`docs/RELATORIO_IMPORTACAO_SQL.md`](docs/RELATORIO_IMPORTACAO_SQL.md) |
| 3. Modelagem e análise | SQL Server (T-SQL) | [`docs/RELATORIO_SQL_ANALISE.md`](docs/RELATORIO_SQL_ANALISE.md) |
| 4. Dashboard interativo | Power BI, DAX | [`docs/RELATORIO_POWERBI.md`](docs/RELATORIO_POWERBI.md) |


## Dataset original

[Campeonato Brasileiro — Kaggle](https://www.kaggle.com/datasets/adaoduque/campeonato-brasileiro-de-futebol/data), com 4 tabelas: partidas, gols, cartões e estatísticas, cobrindo 2003–2025. O dataset foi intencionalmente "sujado" (`dirtify_data.py`) para prática de limpeza de dados com pandas.

## Estrutura do repositório

```
analise-de-times-br/
├── input/                    # CSVs originais do Kaggle
├── data/
│   ├── raw/                   # versão suja (prática)
│   ├── clean_backup/          # gabarito original
│   └── processed/             # dados limpos, prontos para o SQL Server
├── notebooks/                 # scripts/notebooks de limpeza (Python)
├── sql/                       # scripts de criação de tabelas, importação e análise
├── docs/                      # relatórios e guias didáticos
├── powerbi/                   # dashboard Power BI (analiseFlamengo.pbix)
├── reports/                   # exports visuais (screenshots do dashboard)
├── requirements.txt           # bibliotecas Python necessárias
└── README.md
```

## Tecnologias

Python (Pandas, Numpy) · SQL Server (T-SQL) · Power BI (DAX) · Git/GitHub

## Principais achados
- O Flamengo lidera em pontos totais entre os 4 grandes clubes do RJ na base histórica;
- 2019 foi a melhor temporada do clube no recorte analisado com 28 vitórias, se consagrando vencedor do campeonatoç
- Em 2021, Vasco e Botafogo aparecem com poucos jogos registrados — não é erro de dado, e sim reflexo do rebaixamento de ambos à Série B ao final de 2020.
Detalhes completos de cada achado, decisão de limpeza e problema técnico resolvido estão documentados nos relatórios da tabela acima.

## Autor

Matheus Saisse — [github.com/matheus-saisse](https://github.com/matheus-saisse)

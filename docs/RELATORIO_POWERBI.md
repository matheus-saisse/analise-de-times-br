# Dashboard Power BI — Análise de Times BR

**Modo de conexão:** Importar (SQL Server)

---

## 1. Estrutura das páginas

### Visão Geral
Dashboard navegável por temporada, via Slicer de ano. Inclui:
- 4 cards de KPI (pontos, vitórias, jogos, aproveitamento da temporada selecionada)
- Artilheiros da temporada 
- Distribuição de resultado 
- Evolução mensal do saldo de gols dentro da temporada
- Destaques dinâmicos: maior goleada, melhor mês, artilheiro da temporada
- Aproveitamento como mandante x visitante

### Evolução Histórica
Comparação dos 4 times do RJ (Flamengo, Fluminense, Vasco, Botafogo) ao longo de toda a base (2003–2025): gráfico de linha de pontos por ano, com o Flamengo em destaque visual, e cards de aproveitamento histórico por time.

## 2. Medidas DAX principais

| Medida | Função |
|---|---|
| `Pontos na Temporada`, `Vitorias na Temporada`, `Jogos na Temporada` | Agregações simples filtradas por time + contexto de ano do slicer |
| `Aproveitamento na Temporada` | `DIVIDE` + `FORMAT`, evita erro de divisão por zero |
| `Posicao Flamengo RJ` | `ADDCOLUMNS` + `VALUES` + `RANKX` — ranking dos 4 times do RJ por pontos totais |
| `Maior Goleada da Temporada` | `MAXX` + `FILTER` — acha a linha com maior saldo de gols e extrai adversário/placar |
| `Melhor Mes da Temporada` | Agrupamento por mês dentro da própria medida (`ADDCOLUMNS`/`VALUES`) + `SWITCH` pra nome do mês |
| `Artilheiro da Temporada Texto` | Mesmo padrão de "achar o recordista", aplicado a `artilheiros_flamengo_por_ano` |
| `Aproveitamento Como Mandante` / `Como Visitante` | `SUMX` + `SWITCH` pra calcular pontos condicionalmente, filtrado por `mando_de_campo` |

## 3. Design

Tema escuro (`#0D0D0D` fundo de página, `#1A1A1A` cards), com vermelho do Flamengo (`#B4131A`) como única cor de destaque — os demais times do RJ aparecem em cinza neutro (`#B0AFA9`) pra não competir visualmente com o protagonista da análise. Cards com cantos arredondados e borda sutil, escudo do clube como identidade visual no cabeçalho.

## 4. Problemas resolvidos durante a construção

- **DirectQuery não suportava certas combinações de DAX** (`ADDCOLUMNS` + `RANKX`) — resolvido trocando para modo Importar.
- **Unidades de exibição arredondando valores** (ex: "2 Mil" em vez de "2019") em cards de ano/texto — resolvido envolvendo o resultado da medida em `FORMAT()`, que devolve texto e ignora esse arredondamento automático.
- **CTE/relacionamento mal compreendido causando erro "objeto inválido"** — corrigido reforçando que medidas com `WITH`-like patterns (CTEs no SQL) precisam ser executadas como unidade única; no DAX, `VAR/RETURN` cumpre papel semelhante dentro de uma medida.

## 5. Limitações conhecidas

- O dataset cobre **só o Campeonato Brasileiro** — não é possível comparar múltiplas competições (Copa do Brasil, Libertadores, etc.), diferente de alguns dashboards de referência usados como inspiração de design.
- `gols` e `cartoes` cobrem só partidas a partir de 2014; artilheiros e destaques por temporada refletem apenas esse recorte.


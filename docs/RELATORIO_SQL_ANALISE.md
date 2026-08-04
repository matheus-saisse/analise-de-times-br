# Análise em SQL Server — Campeonato Brasileiro (RJ / Flamengo)

**Banco de dados:** `AnaliseTimesBR`
**Objetivo da análise:** evolução dos times do Rio de Janeiro no Brasileirão (2003–2025), com foco no Flamengo

---

## 1. Estrutura das tabelas
| Tabela | Estratégia de chave primária | Observação |
|---|---|---|
| `partidas` | Natural (`ID`) | 1 linha = 1 jogo |
| `estatisticas` | Composta (`partida_id` + `clube`) | 1 linha = estatística de 1 time em 1 jogo |
| `gols` | Surrogate (`GolID`, `IDENTITY`) | Sem coluna naturalmente única |
| `cartoes` | Surrogate (`CartaoID`, `IDENTITY`) | Sem coluna naturalmente única |

Foreign keys ligando tudo de volta em `partidas.ID`: `gols.partida_id`, `cartoes.partida_id`, `estatisticas.partida_id`.


## 2. Views criadas
| View | Descrição |
|---|---|
| `jogos_rj` | Uma linha por time por jogo (perspectiva mandante/visitante unificada via `UNION ALL`), com resultado calculado |
| `evolucao_times_rj` | Agregação por ano de `jogos_rj`: vitórias, empates, derrotas, pontos |
| `artilheiros_flamengo` | Ranking de artilheiros do Flamengo (2014–2025), com normalização de nomes duplicados |

## 3. Investigação de qualidade de dados: nomes de atletas duplicados
Durante a construção do ranking de artilheiros, foi identificado que o dataset original tem **inconsistência na grafia de nomes de atletas** — o mesmo jogador aparece registrado de formas diferentes em partidas diferentes (nome curto vs. nome completo de nascimento).

### Metodologia de investigação
Em vez de corrigir nomes "no olho", foi feita uma busca sistemática por candidatos a duplicata, usando um **self-join** (a tabela de nomes únicos de atletas cruzada com ela mesma) procurando onde um nome está contido dentro de outro. A busca inicial trouxe falsos positivos (ex: "Nan" "dentro" de "Fer**nan**do", por coincidência de substring) 

Cada candidato encontrado foi verificado comparando a **faixa de `partida_id`** das duas variações: sobreposição temporal (ou uma sucessão sem sobreposição, sugerindo mudança de convenção ao longo do tempo).
### Casos confirmados e corrigidos
| Nome no dataset | Nome normalizado | Evidência |
|---|---|---|
| Gabriel Barbosa Almeida | Gabriel Barbosa | Faixas de `partida_id` se sobrepõem; "Almeida" é o sobrenome de nascimento do Gabigol |
| Michael Richard Delgado De Oliveira | Michael | Faixas de `partida_id` não se sobrepõem (mudança de convenção ao longo do tempo); nome bate com o jogador do elenco desde 2021 |

A correção foi implementada com uma **tabela de mapeamento** (`mapeamento_nomes_atletas`) em vez de alterar os dados originais ou usar `CASE WHEN` fixo na view — permite adicionar novos casos verificados no futuro sem editar a lógica da view.

## 4. Principais achados da análise
- Evolução do Flamengo por ano: 2015 foi o pior ano da década (16V/12E/18D); 2018–2019 foi o auge, culminando no titulo do campeonato de 2019 (28 vitórias).
- Comparando os 4 times do RJ, o Flamengo lidera em pontos totais na base.
- Em 2021, Vasco e Botafogo aparecem com poucos jogos registrados (11–13) porque foram **rebaixados para a Série B ao final de 2020** — só restaram os jogos atrasados da temporada 2020 (que se estendeu até fevereiro de 2021 por causa da pandemia).
- Gabriel Barbosa (Gabigol) é o artilheiro histórico do Flamengo no recorte coberto pela base (2014–2025), com 64 gols.

## 5. Limitações conhecidas
- O agrupamento por `YEAR(data)` distorce especificamente 2020 e 2021, por causa do calendário atrasado da pandemia.
- `gols` e `cartoes` só cobrem partidas a partir de abril de 2014.
- `posse_de_bola` e `precisao_passes`, em `estatisticas`, têm cobertura de 38% e 27% respectivamente.
- O ranking de artilheiros reflete só o período coberto por `gols` (2014+), não a carreira completa dos jogadores no clube.
- Podem existir outras inconsistências de nome de atleta no dataset além das 2 corrigidas — a investigação foi feita para o elenco do Flamengo especificamente, não para todos os times da base.

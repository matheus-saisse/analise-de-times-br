# Relatório de Limpeza de Dados — Campeonato Brasileiro (2003–2025)

**Projeto:** Análise de Times BR
**Fonte dos dados:** Kaggle — Campeonato Brasileiro (2003–2025)
**Tabelas processadas:** 4 (partidas, gols, estatísticas, cartões)

---

## 1. Estrutura do projeto

```
analise-de-times-br/
├── input/              # CSVs originais baixados do Kaggle
├── data/
│   ├── raw/             # versão intencionalmente "suja" (prática de limpeza)
│   ├── clean_backup/     # cópia intocada do original (gabarito)
│   └── processed/        # resultado final, limpo e documentado
├── docs                  #Relatório sobre as análises
├── notebooks             #Pasta reservada para os scripts feitos para a limpeza dos dados
├── reports               # Pasta para representações visuais do powerBi (analise que vira posteriormente)
```
> **Nota metodológica:** os dados "sujos" usados neste exercício foram gerados artificialmente a partir do dataset original limpo. O script de "sujeira" é o dirtyfy.py e esta na pasta raw.
---

## 2. Metodologia comum às 4 tabelas

Todas as tabelas seguiram a mesma sequência lógica de limpeza:

- **Carregar** os dados brutos
- **Padronizar nulos disfarçados** (`""`, `"N/A"`, `"-"`, `"null"` → `NaN` real)
- **Limpar texto** (espaços extras, ajustar letras maiúsculas e minúsculas)
- **Corrigir encoding** quebrado (mojibake em nomes com acento)
- **Padronizar categorias** (mesma informação escrita de formas diferentes)
- **Corrigir tipos de dado** (texto que deveria ser número)
- **Tratar outliers** (valores muito distantes dos apresentados no dataset)
- **Remover duplicatas** (por chave única ou composta, utilizando dicionarios quando um metodo do pandas não daria conta de consertat todos de uma vez)
- **Reordenar colunas e ordenar linhas**
- **Relatório de cobertura** e salvar

---

## 3. Tabela `campeonato-brasileiro-full` 

| Métrica | Valor |
|---|---|
| Linhas brutas (sujas) | 9.989 |
| Linhas finais (limpo) | 9.165 |
| Duplicatas removidas | 824 |
| Validação | bate exato com o total original |

### Problemas encontrados e decisões

- **`vencedor` com `"-"`**: não era dado faltando — representava **empate**. Após padronizar nulos, o valor foi restaurado explicitamente com `.fillna("Empate")`.
- **Datas em 7 formatos diferentes** (`DD/MM/AAAA`, `AAAA-MM-DD`, `DD.MM.AAAA`, `DD-MM-AAAA`, `MM/DD/AAAA`, `DD/MM/AA`, `AAAA/MM/DD`): resolvido com um loop que tenta cada formato, um de cada vez, preenchendo só as datas ainda não resolvidas. 
- **Placar como texto sujo** (`" 1 "`, `"2 un"`, `"1,0"`): limpo e convertido para `Int64`.
- **Outliers de placar** (valores como 100, 150, 200 gols): 108 outliers identificados e zerados (`NaN`).
- **Arrecadação**: convertida para número; criada uma coluna adicional `arrecadacao_formatada` em padrão brasileiro (`R$ 1.772.206,00`) só para exibição — a coluna numérica original é mantida intacta para cálculos.
- **Decisão documentada:** as 97 linhas com placar do mandante desconhecido (outlier removido ou dado já ausente) foram **mantidas como `<NA>`**, não preenchidas com 0 nem removidas — preencher mentiria sobre o resultado, e remover perderia informação válida das outras colunas.

---

## 4. Tabela `campeonato-brasileiro-gols`

| Métrica | Valor |
|---|---|
| Linhas brutas (sujas) | 11.793 |
| Linhas finais (limpo) | 10.810 |
| Duplicatas removidas | 983 |
| Validação | 10 linhas a menos que o gabarito (10.820) |

### Problemas encontrados e decisões

- **`tipo_de_gol` com `NaN` significativo**: confirmado por contagem (9.527 nulos + 1.025 "Penalty" + 268 "Gol Contra" = 10.820, batendo exato com o total original) que `NaN` representa **gol normal de jogada**, não dado faltando. Preenchido explicitamente com `"Normal"`.
- **Categorias inconsistentes**: `"Penalty"/"penalti"/"PENALTY"/"Pênalti"` → unificado em `"Pênalti"`; `"Contra"/"autogol"/"Gol Contra"` → unificado em `"Contra"`.
- **Minuto com acréscimo** (`"45+9"`): separado nas duas partes e somado (`45+9 = 54`).
- **Outliers de minuto** (valores como 6200): 149 outliers zerados (limite de 120 minutos).
- **Encoding corrigido**: nomes de atletas com acento quebrado (mojibake) restaurados; validado com busca por caracteres residuais (`0` ocorrências de `Ã` sobrando).
- **Chave composta para duplicatas**: `partida_id + atleta + minuto + clube` (não existe ID único de gol nessa tabela).

### Cobertura de dados
Essa tabela só cobre partidas com `partida_id` de **4.607 a 9.165**, correspondendo a partidas a partir de **19/04/2014** — o dataset original do Kaggle não tem registro de gols detalhado para 2003–2014.

---

## 5. Tabela `campeonato-brasileiro-estatisticas-full`

| Métrica | Valor |
|---|---|
| Linhas brutas (sujas) | 19.979 |
| Linhas finais (limpo) | 18.330 |
| Duplicatas removidas | 1.649 |
| Validação | bate exato com o total original |

### Problemas encontrados e decisões

- **Colunas de percentual sujas** (`posse_de_bola`, `precisao_passes`): vinham com símbolo `%`, sufixo `" un"` e vírgula decimal. Limpas com `.str.replace()` em sequência e convertidas com `pd.to_numeric`.
- **Outliers de percentual**: validação de intervalo (0–100). 0 outliers numéricos encontrados nessa execução, porque a sujeira de multiplicação não conseguiu ser aplicada em cima de strings com `%` (viraram nulo direto, não outlier numérico).
- **`cartao_amarelo` negativo**: 301 outliers (valores como -9, -10) zerados.
- **Chave composta para duplicatas**: `partida_id + clube` (2 linhas por partida, uma por time).

### Achado importante: nulos estruturais do dataset original
Comparando com o backup original (antes de qualquer sujeira aplicada), confirmou-se que:
- `posse_de_bola`: **58,7%** de nulos já no dataset original
- `precisao_passes`: **71,3%** de nulos já no dataset original

Esses nulos **não são efeito da limpeza** — são uma limitação real da fonte de dados ja que a estatística só começou a ser contada após certa data. 

---

## 6. Tabela `campeonato-brasileiro-cartoes`

| Métrica | Valor |
|---|---|
| Linhas brutas (sujas) | 22.838 |
| Linhas finais (limpo) | 20.953 |
| Duplicatas removidas | 1.885 |
| Validação | bate exato com o total original |

### Problemas encontrados e decisões

- **`cartao` com 10 variações de escrita**: unificado em apenas 2 categorias (`Amarelo`, `Vermelho`) via `.map()`. Resultado final: 0 nulos.
- **`posicao` com capitalização inconsistente E um erro de digitação genuíno**: além de variações de maiúscula/minúscula, existia a categoria `"Zagueira"` (22 ocorrências) no próprio dataset original — corrigida para `"Zagueiro"` (posição não tem variação de gênero nesse contexto).
- **`num_camisa`** convertido de texto (`"13.0"`) para `Int64`.
- **`minuto`** tratado com a mesma lógica de acréscimo da tabela de gols; 302 outliers (>100) zerados.
- **Chave composta para duplicatas**: `partida_id + atleta + minuto + cartao`.

---

## 7. Glossário de métodos usados

| Método | Função |
|---|---|
| `df.replace(lista, valor)` | Troca qualquer valor da lista pelo valor novo, na tabela inteira |
| `df[col].str.strip()` | Remove espaços do início/fim de cada célula de texto |
| `df[col].str.title()` / `.str.upper()` | Padroniza o formato do texto |
| `.encode("latin1").decode("utf-8")` | Reverte mojibake (encoding UTF-8 lido incorretamente como Latin-1) |
| `df[col].map(dicionario)` | Unifica escritas de formas diferentes |
| `pd.to_datetime(col, format=, errors="coerce")` | Converte texto em data e o que não bate vira `NaT` |
| `pd.to_numeric(col, errors="coerce")` | Converte texto em número e o que não é número válido vira `NaN` |
| `.astype("Int64")` | Inteiro que aceita valores nulos |
| `df.loc[condição, coluna] = valor` | Altera só as linhas que satisfazem uma condição |
| `df.duplicated(subset=[])` | Marca linhas repetidas |
| `df.drop_duplicates(subset=[])` | Remove as repetidas, mantendo a primeira ocorrência |
| `df.sort_values([]).reset_index(drop=True)` | Ordena linhas e renumera o índice |

---

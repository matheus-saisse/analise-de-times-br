# Importação dos Dados — SQL Server

**Etapa:** Migração dos CSVs limpos para o SQL Server
**Banco:** `AnaliseTimesBR`
**Tabelas:** `partidas`, `gols`, `cartoes`, `estatisticas`

---

## Por que `CREATE TABLE` + `BULK INSERT` em vez do assistente visual

O plano original era usar o assistente **Import Flat File** do SSMS. A partir do SSMS 21/22, a Microsoft removeu esse assistente (dependia do SSIS, cortado nas versões mais novas). A alternativa manual acabou sendo melhor pro aprendizado — força entender a estrutura de cada tabela e suas chaves.

## Staging tables

`gols` e `cartoes` têm uma coluna `IDENTITY` que não existe no CSV. `BULK INSERT` não aceita lista de colunas entre parênteses (isso é sintaxe de `INSERT INTO`), então a solução foi:

1. Criar uma tabela temporária idêntica ao CSV (sem a coluna `IDENTITY`)
2. `BULK INSERT` nela
3. `INSERT INTO tabela_final (colunas) SELECT colunas FROM staging`
4. `DROP TABLE staging`

## Problemas encontrados 

**1. Sintaxe inválida no `BULK INSERT`** — tentativa de usar lista de colunas entre parênteses, que não existe nesse comando. Resolvido com staging table.

**2. Caminho de arquivo errado** — bloco de `partidas` apontando pro CSV de `estatisticas` por engano.

**3. Erro genérico `IID_IColumnsInfo`** — mensagem enganosa, mesma causa aparente pra problemas diferentes. Testadas 3 hipóteses até achar a real:
   - Permissão de pasta (não era o caso aqui, mas causa legítima em outros cenários)
   - BOM (Byte Order Mark) no início do CSV
   - **Causa real**: índice do pandas vazando pro CSV (coluna extra sem nome no início), deslocando todas as colunas em 1 posição
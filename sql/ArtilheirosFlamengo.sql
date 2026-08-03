--- OBS: o data set original tem algumas inconsistencias com nomes de jogadores
--- exemplo: Gabriel Barbosa e Gabriel Barbosa Almeida sao a mesma pessoa
--- Assim criarei uma tabela de mapeamento por gols, considerando os noms ja verificados, nao excluindo nenhum dado.
CREATE VIEW artilheiros_flamengo AS
SELECT
    COALESCE(m.nome_normalizado, g.atleta) AS atleta,
    COUNT(*) AS total_gols
FROM gols AS g
LEFT JOIN mapeamento_nomes_atletas AS m
    ON g.atleta = m.nome_no_dataset
WHERE g.clube = 'Flamengo'
    AND g.atleta IS NOT NULL
GROUP BY COALESCE(m.nome_normalizado, g.atleta);
GO

SELECT TOP 10 *
FROM artilheiros_flamengo
ORDER BY total_gols DESC;
GO


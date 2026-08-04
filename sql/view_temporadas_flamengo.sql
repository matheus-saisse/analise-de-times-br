--- view destinada a evolucao das temporadas do flamengo exclusivamente

CREATE VIEW temporadas_flamengo AS
SELECT DISTINCT YEAR(data)AS ano
FROM partidas
WHERE (mandante = 'Flamengo' OR visitante = 'Flamengo')

--- view destinada ao artilheiros do flamengo por temporada, quebrada por ano

CREATE VIEW artilheiros_flamengo_por_ano AS
SELECT 
    YEAR(data) AS ano, 
    COALESCE(m.nome_normalizado, g.atleta) AS atleta,
     COUNT(*) AS gols
FROM gols as g
JOIN partidas AS p
    ON g.partida_id = p.ID
--- utiliza a tabela de mapeamento utilizada anteriormente
LEFT JOIN mapeamento_nomes_atletas AS m
    ON g.atleta = m.nome_no_dataset
WHERE g.clube = 'Flamengo'
    AND g.atleta IS NOT NULL
GROUP BY
    YEAR(p.data),
    COALESCE(m.nome_normalizado, g.atleta);

SELECT TOP 20 *
FROM artilheiros_flamengo_por_ano
ORDER BY ano DESC, gols DESC;
GO
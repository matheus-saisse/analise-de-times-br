CREATE VIEW desempenho_detalhado_flamengo AS
SELECT
    ID AS partida_id,
    data,
    YEAR(data) AS ano,
    MONTH(data) AS mes,
    visitante AS adversario,
    mandante_Placar AS gols_marcados,
    visitante_Placar AS gols_sofridos,
    (mandante_Placar - visitante_Placar) AS saldo_gols,
    CASE
        WHEN mandante_Placar > visitante_Placar THEN 'Vitoria'
        WHEN mandante_Placar = visitante_Placar THEN 'Empate'
        ELSE 'Derrota'
    END AS resultado
FROM partidas
WHERE mandante = 'Flamengo'
    AND mandante_Placar IS NOT NULL
 
UNION ALL
 
SELECT
    ID AS partida_id,
    data,
    YEAR(data) AS ano,
    MONTH(data) AS mes,
    mandante AS adversario,
    visitante_Placar AS gols_marcados,
    mandante_Placar AS gols_sofridos,
    (visitante_Placar - mandante_Placar) AS saldo_gols,
    CASE
        WHEN visitante_Placar > mandante_Placar THEN 'Vitoria'
        WHEN visitante_Placar = mandante_Placar THEN 'Empate'
        ELSE 'Derrota'
    END AS resultado
FROM partidas
WHERE visitante = 'Flamengo'
    AND visitante_Placar IS NOT NULL;


SELECT TOP 10 *
FROM desempenho_detalhado_flamengo
ORDER BY saldo_gols DESC;
GO
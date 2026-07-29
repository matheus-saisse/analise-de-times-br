-- UNION ALL que junta os jogos em que o time foi mandante e os que foi visitante, 

WITH jogos_times_rj AS(
	
	SELECT 
		YEAR(data) AS ano,
		mandante AS time,
		CASE 
			WHEN mandante_Placar > visitante_Placar THEN 'Vitoria'
            WHEN mandante_Placar = visitante_Placar THEN 'Empate'
            ELSE 'Derrota'
        END AS resultado
    FROM partidas
    WHERE mandante IN ('Flamengo', 'Fluminense', 'Vasco', 'Botafogo-Rj')
        AND mandante_Placar IS NOT NULL

	UNION ALL

	SELECT
		YEAR(data) AS ano,
		visitante AS time,
		CASE
			WHEN visitante_Placar > mandante_Placar THEN 'Vitoria'
            WHEN visitante_Placar = mandante_Placar THEN 'Empate'
            ELSE 'Derrota'
        END AS resultado
    FROM partidas
    WHERE visitante IN ('Flamengo', 'Fluminense', 'Vasco', 'Botafogo-Rj')
        AND visitante_Placar IS NOT NULL
)

--- select que gera a tabela somando vitorias, derrotas e empates dos times, considerando a evolução dos 4 times do rj ao longo dos anos, todos agrupados por ano e time.
SELECT
	ano,
	time,
	SUM(CASE WHEN resultado = 'Vitoria' THEN 1 ELSE 0 END) AS vitorias,
	SUM(CASE WHEN resultado = 'Empate' THEN 1 ELSE 0 END) AS empates,
	SUM(CASE WHEN resultado = 'Derrota' THEN 1 ELSE 0 END) AS derrotas,
	SUM(CASE	
		WHEN resultado = 'Vitoria' THEN 3
		WHEN resultado = 'Empate' THEN 1
		ELSE 0
	END) AS pontos,
	COUNT(*) AS jogos_disputados
	FROM jogos_times_rj
	GROUP BY ano, time
	ORDER BY ano, time;
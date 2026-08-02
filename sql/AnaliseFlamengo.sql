-- INNER JOIN juntando os dados da tabela estatistica para os dados da tabela partida
-- desconsiderando todos os times que nao sejam o flamengo.
SELECT
	p.ID,
	p.data,
	p.mandante,
	p.visitante,
	e.clube,
	e.posse_de_bola,
	e.chutes
FROM partidas AS p
INNER JOIN estatisticas AS e
	ON p.ID = e.partida_id
WHERE e.clube = 'Flamengo'
ORDER BY p.data;

-- LEFT JOIN contando todos os gols que o flamengo fez por partida ordenados por ano
-- uso do LEFT JOIN se da pois usando INNER, jogos que o flamengo nao fez gols desapareceriam.
SELECT
	p.ID,
	p.data,
	p.mandante,
	p.visitante,
	COUNT(g.GolID) AS gols_do_flamengo
FROM partidas AS p
LEFT JOIN gols AS g
	ON p.ID = G.partida_id
	AND g.clube = 'Flamengo'
WHERE p.mandante = 'Flamengo' OR p.visitante = 'Flamengo'
GROUP BY p.ID, p.data, p.mandante, p.visitante
ORDER BY p.data;

--resultado de cada jogo do flamengo.
SELECT 
	p.ID,
	P.data,
	YEAR(p.data) as ano,
	CASE
		WHEN p.mandante = 'Flamengo' AND p.mandante_Placar > p.visitante_Placar THEN 'Vitoria'
		WHEN p.visitante = 'Flamengo' AND p.visitante_Placar > p.mandante_Placar THEN 'Vitoria'
		WHEN p.mandante_Placar = p.visitante_Placar THEN 'Empate'
		ELSE 'Derrota'
	END AS resultado
FROM partidas AS p
WHERE (p.mandante = 'Flamengo' OR p.visitante = 'Flamengo')
AND p.tecnico_mandante IS NOT NULL
ORDER BY p.data;

--evolução do flamengo ao longo dos anos juntando o groupby ao passo 3
SELECT
    YEAR(p.data) AS ano,
    SUM(CASE
        WHEN p.mandante = 'Flamengo' AND p.mandante_Placar > p.visitante_Placar THEN 1
        WHEN p.visitante = 'Flamengo' AND p.visitante_Placar > p.mandante_Placar THEN 1
        ELSE 0
    END) AS vitorias,
    SUM(CASE
        WHEN p.mandante_Placar = p.visitante_Placar THEN 1
        ELSE 0
    END) AS empates,
    SUM(CASE
        WHEN p.mandante = 'Flamengo' AND p.mandante_Placar < p.visitante_Placar THEN 1
        WHEN p.visitante = 'Flamengo' AND p.visitante_Placar < p.mandante_Placar THEN 1
        ELSE 0
    END) AS derrotas,
    COUNT(*) AS jogos_disputados
FROM partidas AS p
WHERE (p.mandante = 'Flamengo' OR p.visitante = 'Flamengo')
    AND p.mandante_Placar IS NOT NULL
GROUP BY YEAR(p.data)
ORDER BY ano;

-- correção dos 47 jogos flamengo

SELECT
    ID,
    COUNT(*) AS quantas_vezes_aparece
FROM partidas
WHERE (mandante = 'Flamengo' OR visitante = 'Flamengo')
    AND YEAR(data) = 2021
GROUP BY ID
HAVING COUNT(*) > 1;


SELECT
    time,
    COUNT(*) AS total_jogos
FROM (
    SELECT mandante AS time FROM partidas WHERE YEAR(data) = 2021
    UNION ALL
    SELECT visitante AS time FROM partidas WHERE YEAR(data) = 2021
) AS todos_os_times
GROUP BY time
ORDER BY total_jogos DESC;


SELECT DISTINCT mandante, LEN(mandante) AS tamanho
FROM partidas
WHERE mandante LIKE '%Flamengo%'

UNION

SELECT DISTINCT visitante, LEN(visitante) AS tamanho
FROM partidas
WHERE visitante LIKE '%Flamengo%';

-- por conta da pandemia o ano do futebol so começou em agosto de 2020 e terminou em 2021, nao é uma anomalia no codigo e sim uma questao de agrupamento por data visto que o brasileirao de 2020 foi ate 2021. 
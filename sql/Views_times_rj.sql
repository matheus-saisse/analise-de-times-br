--- Criação de views no sql, essa consulta tem o intuito da comp dos times do rj, porem com foco em aprender como as views funcionam.
--- a criação de uma view gera uma forma mais rapida de vizualizar uma tabela, minimizando o tamanho do codigo.

--- View qqqie separa os times do rj como mandante e visitante, fazendo um union all ( igual ao outro codigo)

CREATE VIEW jogos_rj AS
SELECT
	ID AS partida_id,
	YEAR(data) AS ano,
    data,
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
    ID AS partida_id,
    YEAR(data) AS ano,
    data,
    visitante AS time,
    CASE
        WHEN visitante_Placar > mandante_Placar THEN 'Vitoria'
        WHEN visitante_Placar = mandante_Placar THEN 'Empate'
        ELSE 'Derrota'
    END AS resultado
FROM partidas
WHERE visitante IN ('Flamengo', 'Fluminense', 'Vasco', 'Botafogo-Rj')
    AND visitante_Placar IS NOT NULL;
GO
--- essa view retorna se o fla,vas,flu ou bot empataram, perderam ou ganharam todos os jogos desde 2003.
SELECT * FROM jogos_rj ORDER BY data;
GO		


----------------comentar 
CREATE VIEW evolucao_times_rj AS
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
        COUNT(*) AS jogos_dispuatados
    FROM jogos_rj
    GROUP BY ano,time;
    GO
--- evolução por vitorias, empates, derrotas e pontos do flamengo desde 2003.
SELECT * FROM evolucao_times_rj
WHERE time = 'Flamengo'
ORDER BY ano;
GO

--- evolução por vitorias, empates, derrotas e pontos de todos os times do rj desde 2003.
SELECT * FROM evolucao_times_rj
WHERE ano = 2019
ORDER BY pontos DESC;
GO









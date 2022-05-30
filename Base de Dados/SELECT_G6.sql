-- Pesquisar informação sobre utente p.e: UT0006
SELECT UTENTE.*
    FROM UTENTE
    WHERE UTENTE.ID_utente='UT0006';
    
-- Pesquisar informação sobre médico p.e.: MD0014
SELECT MEDICO.*
    FROM MEDICO
    WHERE MEDICO.ID_medico='MD0014';
    
-- Pesquisar informação sobre técnico p.e.: TC0009
SELECT TECNICO.*
    FROM TECNICO
    WHERE TECNICO.ID_tecnico='TC0009';
    
-- Pesquisa as consultas para determinado dia p.e.: 2020-01-30
SELECT CONSULTA.*
	FROM CONSULTA
    WHERE CONSULTA.data_hora LIKE '2020-01-30%';
    
-- Pesquisa as consultas de um determinado médico para uma determinada semana
-- p.e.: MD0009 na semana de 4 FEV a 8 FEV
SELECT CONSULTA.*
	FROM CONSULTA
    WHERE CONSULTA.ID_medico='MD0009' AND (CONSULTA.data_hora BETWEEN '2020-02-04 00H00' AND '2020-02-08 23H59');
    
-- Pesquisa os exames para determinado dia p.e.: 2020-01-30
SELECT EXAME.*
	FROM EXAME
    WHERE EXAME.datahora LIKE '2020-01-30%';
    
-- Pesquisa os exames de um determinado técnico para uma determinada semana
-- p.e.: TC0015 na semana de 4 FEV a 8 FEV
SELECT EXAME.*
	FROM EXAME
    WHERE EXAME.ID_tecnico='TC0015' AND (EXAME.datahora BETWEEN '2020-02-04 00H00' AND '2020-02-08 23H59');
    
-- Pesquisa os exames que um determinado médico marcou para uma determinada semana
-- p.e.: MD0004 na semana de 4 FEV a 8 FEV
SELECT EXAME.*
	FROM EXAME
    WHERE EXAME.ID_medico='MD0004' AND (EXAME.datahora BETWEEN '2020-02-04 00H00' AND '2020-02-08 23H59');
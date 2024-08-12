-- Consultando todos os dados da tabela TMDB

select * from tmdb;

-- Exibindo todos os dados da tabela CSV

select * from csv;

-- Consultando se há dados duplicados no tmdb
SELECT t.*
FROM tmdb t
JOIN (
    SELECT id
    FROM tmdb
    GROUP BY id
    HAVING COUNT(id) > 1
) duplicadas ON t.id = duplicadas.id
ORDER BY t.id

-- Realizando junção das duas tabelas
select * from tmdb join csv on tmdb.id = csv.id;

-- Somando toda a coluna orçamento
select sum(orcamento) orcamento_total count(*) quantidade_linhas from tmdb;
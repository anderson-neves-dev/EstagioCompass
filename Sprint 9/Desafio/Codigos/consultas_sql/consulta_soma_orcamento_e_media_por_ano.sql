SELECT 
    SUM(soma.orcamento) AS soma_orcamento, 
    AVG(soma.orcamento) AS media_orcamento, 
    count(*) quantidade_filmes, 
    soma.ano_lancamento
FROM (
    SELECT AVG(ff.orcamento) AS orcamento, df.ano_lancamento
    FROM fato_filme ff
    JOIN dim_filme df ON ff.id_filme = df.id_filme
    GROUP BY ff.id_filme, df.ano_lancamento
) AS soma
GROUP BY soma.ano_lancamento
order by media_orcamento;

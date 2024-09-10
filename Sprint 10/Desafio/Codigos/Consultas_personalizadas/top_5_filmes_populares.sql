SELECT 
    df.id_filme AS id_filme, 
    max(ff.popularidade_tmdb) as popularidade_top_5,
    array_join(array_agg(DISTINCT dg.genero ORDER BY dg.genero ASC), ', ') AS genero_concatenado
FROM "desafio-final-filmes-modelo-dimensional".fato_filme ff
JOIN "desafio-final-filmes-modelo-dimensional".dim_filme df ON ff.id_filme = df.id_filme
JOIN "desafio-final-filmes-modelo-dimensional".dim_genero dg ON dg.id_genero = ff.id_genero 
GROUP BY df.id_filme
order by popularidade_top_5 desc
limit 5

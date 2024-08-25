SELECT *
FROM dim_pais dp
JOIN fato_filme ff ON ff.id_pais = dp.id_pais
JOIN dim_filme df ON df.id_filme = ff.id_filme
JOIN dim_genero dg ON dg.id_genero = ff.id_genero;
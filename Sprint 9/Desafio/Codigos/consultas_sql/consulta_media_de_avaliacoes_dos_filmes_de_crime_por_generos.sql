select 
    round(avg(ff.popularidade_TMDB), 3) as popularidade, 
    round(avg(ff.nota_media_IMDB), 1) as imdb, 
    round(avg(ff.nota_media_TMDB), 1)as tmdb, 
    dg.genero 
from 
    fato_filme ff 
join 
    dim_genero dg 
on 
    dg.id_genero = ff.id_genero 
where 
    ff.id_filme in (
        select 
            id_filme 
        from 
            fato_filme ff 
        where 
            ff.id_genero = 80 
    ) 
    and ff.id_genero != 80 
group by 
    dg.id_genero, dg.genero 
having count(*) >= 10
order by 
    imdb desc;

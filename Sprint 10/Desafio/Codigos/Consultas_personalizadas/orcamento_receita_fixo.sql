select 
    id_filme,
    avg(orcamento) Orcamento, 
    avg(receita) Receita 
from "desafio-final-filmes-modelo-dimensional".fato_filme 
group by id_filme
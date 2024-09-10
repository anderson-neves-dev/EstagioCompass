# Sobre o desafio da Sprint 10
- O desafio desta sprint consiste na entrega da última etapa do desafio final. Nesta fase, o objetivo é criar uma dashboard com os dados contidos da camada refined para obter insights utilizando a ferramenta da aws QuickSight.
    
## 🏆 Tema Desafio final
#### Como tema do desafio final, escolhi analisar as combinações entre gêneros cinematográficos com filmes de crime de 2012 à 2022.

#### Busco responder as seguintes questões:

- Quais os gêneros cinematográfico que mais combinam com os filmes de crime?  Existem gêneros que combinados com o de crime são mais lucrativos ou mais populares?

- Os cinco filmes de crime mais populares e os cinco mais lucrativos possuem um padrão de gêneros combinados?
    
## 📋 Etapas

### 1️⃣ Criar um conjunto de dados no QuickSight

- A primeira etapa foi criar um novo conjunto de dados na ferramenta da AWS QuickSight, esses dados foram provindos da camada refined. 
- Ao analisar bem os dados, percebi que uma informação muito importante para gerar insights valiosos era a de receita e até então não tinha esse dado, também foquei a minha análise somente em filmes de crime e não mais com os de guerra. Então foi necessário realizar uma modificação na minha função lambda de ingestão dos dados do TMDB da camada Raw Zone para conseguir ter a informação da receita dos filmes, além de pegar somente os dados dos filmes de crime. 
- O código com as alterações da função lambda está em: [Codigos/lambda/ingestao-dados-do-tmdb-desafio-final.py](Codigos/lambda/ingestao-dados-do-tmdb-desafio-final.py)
- Evidência de execução da função lambda alterada: 
  ![](Evidencias/print_evidencia_funcao_lambda_executada.png)
  ![](Evidencias/print_evidencia_de_execucao_funcao_lambda_dados_tmdb_no_bucket.png)
  ![](Evidencias/print_evidencia_funcao_lambda_json.png)
- Após essa mudança, realizei o processamento e refinamento desses dados da camada trusted e refined.
  - Códigos dos jobs em spark alterados do processamento da camada trusted e refined: [Codigos/jobs/](Codigos/jobs/)
  - Evidência de execução dos jobs alterados na AWS Glue:
    ![](Evidencias/print_evidencia_de_execucao_job_tmdb_processamento_trusted.png)
    ![](Evidencias/print_evidencia_de_execucao_job_csv_processamento_trusted.png)
    ![](Evidencias/print_evidencia_de_execucao_job_processamento_refined.png)
- Com os arquivos parquet dimensionados na camada refined no bucket s3, executei novamente o crawler da etapa anterior para gerar as tabelas no banco de dados.
  ![](Evidencias/print_evidencia_crawler_executado_com_sucesso.png)
- Evidência dos dados no Athena:
  ![](Evidencias/print_evidencia_database_com_dados_dimensionais_no_athena.png)
- Com essas mudanças os dados ficaram no seguinte modelo dimensional na camada refined:
![](Evidencias/modelo_dimensional.png)

- Com os dados completos na camada refined e catalogados como um database, no QuickSight criei um conjunto de dados com a fonte Athena, selecionei o banco de dados que estão as minhas tabelas e adicionei a tabela fato.
- Após isso, adicionei a tabela dimensão de filmes e de gêneros, realizando a junção dessas tabelas com a tabela fato através de um inner join entre as chaves identificadoras que cada uma corresponde.
- Para realizar algumas análises, adicionei dados com consultas personalizadas em SQL. 
  - Uma dessas consultas, foi para filtragem dos 5 filmes mais populares, selecionando apenas o id desses filmes, popularidade e concatenando os gêneros desses filmes.
  ![](Evidencias/print_conjunto_de_dados_consulta_personalizada_top5_filmes_populares.png)
  -  Fiz a mesma coisa para os 5 filmes mais lucrativos pegando id, lucro e os gêneros concatenados.
    ![](Evidencias/print_conjunto_de_dados_consulta_personalizada_top5_filmes_lucrativos.png)
  - Também realizei uma consulta SQL personalizada para extrair as informações de orçamento e receita dos filmes sem repetir esse valores que são fixos e se repetem na tabela fato devido a coluna id_genero que é multivalorada. Dessa forma, os valores fixos não são repetidos ao se unir com a tabela fato que contém os gêneros.
    ![](Evidencias/print_conjunto_de_dados_consulta_personalizada_top5_filmes_orcamento_receita_fixo.png)
  - Foi realizado a junção dessas consultas personalizadas por left join, para não implicar em uma filtragem geral dos dados.

- Por fim, o conjunto de dados no QuickSight ficou da seguinte forma:
![](Evidencias/print_conjunto_de_dados_quicksight.png)

### 2️⃣ Criação dos gráficos
- Com o conjunto de dados estabelecido, o próximo passo foi criar os gráficos da minha dashboard sobre o meu tema.
- o Primeiro passo foi criar um filtro geral para a minha planilha para remover os filmes que somente são do gênero de crime, pois minha analise visa a combinação dos gêneros com o de crime. Apenas dois filmes foram excluidos com o filtro.
![](Evidencias/print_quicksight_filtro_geral.png) 

- Adicionei alguns KPI: 
   - Quantidade de filmes analisados:
  ![](Evidencias/print_quicksight_KPI_qtd_filmes.png)
    - Quantidade de gênero:
  ![](Evidencias/print_quicksight_KPI_qtd_genero.png)
    - Média geral de popularidade:
    ![](Evidencias/print_quicksight_KPI_media_popularidade.png)
    - Média geral de avaliações do IMDB e do TMDB:
    ![](Evidencias/print_quicksight_media_de_avaliacao_IMDB.png)
    ![](Evidencias/print_quicksight_media_de_avaliacao_TMDB.png)
    - Soma total de receita e orçamento, com aumento da margem de lucro em porcentagem.
    ![](Evidencias/print_quicksight_KPI_total_receita_e_orcamento.png)
- Nuvem de palavras dos gêneros com a frequencia que eles apareceram nos filmes de crime.
  ![](Evidencias/print_quicksight_nuvem_de_palavras_genero.png)
- Gráfico de barras horizontal com a quantidade de filmes de crime que os gêneros aparecem.
  ![](Evidencias/print_quicksight_grafico_barras_quantidade_filmes_crime_com_generos.png)
- Gráfico de barras horizontal com a média de popularidade por gênero dos filmes de crime.
    ![](Evidencias/print_quicksight_grafico_barras_horizontal_popularidade_media_por_genero.png)
- Gráfico de barras empilhadas horizontal com as medias de avaliações de cada plataforma por gênero.
  ![](Evidencias/print_quicksight_grafico_barras_empilhadas_media_de_avaliacoes_por_genero.png)
- Gráfico de barras da média de margem de lucratividade dos filmes de crime por gêneros. Obs.: Para essa margem percentual criei um campo calculado entre a receita e orçamento dos filmes.
  ![](Evidencias/print_quicksight_campo_calculado_margem_percentual_de_lucro.png)
  ![](Evidencias/print_quicksight_media_percentual_de_lucratividade_por_genero.png)
- Gráfico de barras horizontal da média de orçamento dos filmes de crime por gênero.
  ![](Evidencias/print_quicksight_grafico_barras_vertical_media_orcamento_por_genero.png)
- Gráfico de barras horizontal dos 5 filmes de crime mais populares do período.
  ![](Evidencias/print_quicksight_grafico_horizontal_5_filmes_crime_mais_populares.png)
- Gráfico de barras horizontal dos 5 filmes de crime que tiveram os maiores lucros do período.
  ![](Evidencias/print_quicksight_grafico_barras_horizontal_5_filmes_mais_lucrativos.png)
- Tabela dos 5 filmes mais populares do período.
  ![](Evidencias/print_quicksight_tabela_5_filmes_mais_populares.png)
- Tabela dos 5 filmes mais lucrativos do período.
  ![](Evidencias/print_quicksight_tabela_5_filmes_mais_lucrativo.png)


### 3️⃣ Organização da dashboard

- Com os gráficos prontos, organizei a minha dashboard utilizando o método "Z", com um layout organizado e fluído para raciocínio para analise.
- Por fim, a dashboard ficou da seguinte forma:
  ![](Evidencias/dashboard_parte1.png)
  ![](Evidencias/dashboard_parte2.png)
  ![](Evidencias/dahsboard_parte3.png)
  ![](Evidencias/dashboard_parte4.png)
 - PDF da dashboard: [Evidencias/Analise_de_combinacoes_entre_generos_cinematograficos_com_filmes_de_crime_de_2012_a_2022.pdf](Evidencias/Analise_de_combinacoes_entre_generos_cinematograficos_com_filmes_de_crime_de_2012_a_2022.pdf.pdf)
### 4️⃣ Insights analisados

- Os gêneros que mais aparecem em filmes de crime são Suspense, Ação, Drama e Comédia, seguidos de Mistério e Aventura​.
- Ação, Suspense e Drama são os gêneros mais frequentemente combinados com o gênero crime nos filmes mais populares e lucrativos. Filmes de crime combinados com esses gêneros tendem a ser mais lucrativos, como visto nos exemplos de filmes como Furious 7, The Fate of the Furious e Joker, que estão entre os mais lucrativos.
- Filmes de crime combinados com Ação e Suspense são especialmente lucrativos, com margens de lucro acima de 400%, enquanto filmes de Drama e Faroeste também apresentam margens de lucro superiores a 350%.
- Gêneros como Comédia e Família também se destacam em termos de popularidade, mas a combinação com o gênero Suspense traz uma popularidade mais consistente nos filmes de crime.
- Gênero Faroeste é pouco frequente em filmes de crime, mas altamente lucrativo, com uma margem de lucro de 363,5% e uma boa recepção crítica, com média de 6,9 no TMDB e IMDB. Seu baixo orçamento médio de $12,55 milhões contribui para um retorno financeiro expressivo.
- Filmes de Ficção Científica e Crime, embora sejam populares, apresentam uma margem de lucro baixa. Isso se deve ao fato de terem um orçamento muito alto, o que limita o retorno financeiro. Mesmo com uma boa aceitação do público, os altos custos de produção fazem com que o lucro final seja significativamente menor em comparação a outros gêneros.
- Gêneros como Terror e Documentário apresentam uma margem de lucro negativa em filmes de crime. No caso do Terror, a margem é de -15,8%, e para Documentário, é de -5%. Isso indica que os filmes desses gêneros, quando combinados com crime, não conseguem recuperar o investimento, resultando em prejuízos financeiros, apesar de serem nichos com potenciais audiências.

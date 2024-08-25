# Sobre o desafio
- O desafio desta sprint consiste na entrega da quarta etapa do desafio final, que envolve o processamento da Camada Refined. Nesta fase, o objetivo é assegurar que os dados sejam confiáveis e realizar a modelagem multidimensional dos dados contidos na camada trusted da etapa 3 do desafio.
    
## 🏆 Tema Desafio final

#### Como tema do desafio final, escolhi analisar os filmes dos gêneros crime e guerra lançados entre 2012 e 2022. O foco da análise é entender a relação entre a média de avaliação, popularidade e orçamento, os generos que mais combinam e as tendências de orçamento e popularidade.

#### Busco responder as seguintes questões:

- Qual é a média de avaliação e a média de popularidade dos 10 filmes com os maiores orçamentos lançados entre 2012 e 2022 para cada um dos gêneros guerra e crime? Os filmes de guerra e crime analisados têm uma aceitação geral positiva de acordo com a média de popularidade para seus respectivos gêneros?

- Quais os gêneros que mais "combinam" com os gêneros de crime e guerra? 

- Quais os paises que mais produziram filmes desses generos diante esse intervalo de tempo?

- A média dos orçamentos para filmes dos gêneros 'guerra' e 'crime' aumentou de 2012 a 2022? E a média de popularidade desses filmes seguiu uma tendência similar durante o mesmo período?
    
## 📋 Etapas

### 1️⃣ Criar o modelo dimensional para os dados da camada trusted

- A primeira etapa foi analisar todos os meus dados contidos na camada Trusted Zone e gerar o modelo dimensional dos dados com as tabelas dimensões e a tabela fato. 
- Meus dados inicialmente na camada trusted estavam da seguinte forma: 
![](Evidencias/esquema_dos_dados_na_camada_trusted.jpeg)
- Evidência dos dados na camada trusted: 
![](Evidencias/print_envidencia_camada_trusted_dados_csv.png)
![](Evidencias/print_envidencia_camada_trusted_dados_tmdb.png)
- Evidência de consultas dos dados da camada trusted no Athena:
![](Evidencias/print_evidencia_consulta_athena_dados_camada_trusted_tmdb.png)
![](Evidencias/print_evidencia_consulta_athena_dados_camada_trusted_csv.png)

- Após analisar os dados na camada trusted e relacionar como eles iriam responder as minhas questões, criei o seguinte modelo dimensional:
![](Evidencias/modelo_dimensional.jpeg)
- Então, vou estar criando as seguintes tabelas com os atributos:
  - Dimensão filme:
    - id_filme;
    - Título principal;
    - Título original;
    - Ano de lançamento;
    - Poster link.
  - Dimensão país:
    - id_pais;
    - Sígla dos países.
  - Dimensão gênero:
    - id_genero;
    - Nome dos gêneros.
  - Fato filme:
    - id_filme;
    - id_genero;
    - id_pais;
    - Orçamento;
    - Popularidade do tmdb;
    - Nota média do tmdb;
    - Nota média do imdb;
    - Número de votos tmdb;
    - Número de votos imdb;   


### 2️⃣ Criar o job para processamento da camada Refined

- Após definir o esquema dimensional que iria utilizar, o segundo passo foi criar o job responsável por realizar o processamento de modelagem desses dados utilizando spark no ETL job dos serviços AWS Glue.
- Configurações do job:
![](Evidencias/print_configuracao_job_parte_1.png)
- Adicionei uma IAM role que foi criada na terceira etapa para conseguir utilizar outros serviços da AWS. As políticas foram:
    - AmazonS3FullAcess;
    - AWSGlueConsoleFullAcess;
    - AWSLakeFormationAdmin;
    - CloudWatchFullAcess.
![](Evidencias/print_IAM_role.png)
![](Evidencias/print_configuracao_job_parte_2.png)

- Nos parâmetros, adicionei `S3_INPUT_CSV_PATH` com o caminho da camada trusted no bucket onde estão os arquivos parquet provindos do CSV, que estão no caminho: `s3://desafio-final-filmes-e-series-anderson-neves/Trusted/CSV/` e `S3_INPUT_TMDB_PATH` com os arquivos parquet com os dados provindos da api TMDB que estão no caminho: `s3://desafio-final-filmes-e-series-anderson-neves/Trusted/TMDB`

- Adicionei também aos parâmetros `S3_TARGET_PATH` com o caminho alvo onde vou exportar os meus dataframes dimensionados em arquivos parquet, que vão ficar na camada Refined: `s3://desafio-final-filmes-e-series-anderson-neves/Refined`
![](Evidencias/print_configuracao_job_parte_3.png)

- Após configurar o job, criei o script em spark para a modelagem multidimensional dos dados.
- Primeiramente, o código contém a importação das bibliotecas que irei utilizar
    ```python
    import sys
    from awsglue.transforms import *
    from awsglue.utils import getResolvedOptions
    from pyspark.context import SparkContext
    from awsglue.context import GlueContext
    from awsglue.job import Job
    from pyspark.sql.functions import split, explode, col, monotonically_increasing_id, concat, lit
    from pyspark.sql.types import IntegerType
    ```
- Extrai os parâmetros que vou trabalhar e inicializei todos os contextos de trabalho com spark e o glue (configurações padrões).
    ```python
    args = getResolvedOptions(sys.argv, ['JOB_NAME', args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_CSV_PATH','S3_INPUT_TMDB_PATH', 'S3_TARGET_PATH'])
    sc = SparkContext()
    glueContext = GlueContext(sc)
    spark = glueContext.spark_session
    job = Job(glueContext)
    job.init(args['JOB_NAME'], args)
    ```
- Defini uma variável para armazenar os caminhos onde meus arquivos parquet estão, o diretório datado referecia o último tratamento realizado na camada trusted.
    ```python
    S3_INPUT_CSV_PATH = args['S3_INPUT_CSV_PATH']
    S3_INPUT_TMDB_PATH = args['S3_INPUT_TMDB_PATH'] + '/2024/08/11/' 
    ```

- Realizando a leitura e transformando meus arquivos parquet em dataframes.
    ```python
    df_csv = spark.read.parquet(S3_INPUT_CSV_PATH)
    df_tmdb = spark.read.parquet(S3_INPUT_TMDB_PATH)
    ```
- Imprimo o esquema do dataFrame antes da formatação.
    ```python
    df_csv.printSchema()
    df_tmdb.printSchema()
    ```
- Comecei a modelagem dos dados pela dimensão país. 
- Primeiramente selecionei apenas a coluna `paisOrigem` dos dados do tmdb
    ```python
    df_pais = df_tmdb.select("paisOrigem")
    ```
- Com os dados de país, transformei a coluna 'paisOrigem' em múltiplas linhas, uma para cada pais, pois alguns filmes são internacionais e os países estão agrupados na mesma linha separados por vírgula, assim como os de gênero. Para isso utilizei a função `explode()` em conjunto com `split()` para "explodir" as linhas com mais de um valor separados por vírgula.
    ```python
    df_pais = df_pais.withColumn("paisOrigem", explode(split(col("paisOrigem"), ",")))
    ```
- Como os dados de país e gênero estavam agrupados:
![](Evidencias/print_dados_pais_e_genero_agrupados_como_lista.png)
- Removendo linhas duplicadas para conter apenas um país por linha e removendo linhas vazias que não possuem países.
    ```python
    df_pais = df_pais.dropDuplicates()
    df_pais = df_pais.filter(col("paisOrigem") != "")
    ```

- Adicionei uma coluna id_pais com um id para cada país utilizando a função `monotonically_increasing_id()`.
    ```python
    df_pais = df_pais.withColumn("id_pais", monotonically_increasing_id())
    ```
- Transformei a coluna 'paisOrigem' em múltiplas linhas, uma para cada pais no data frame com os dados tmdb, adicionando esses dados em um novo dataframe geral chamando df_filme que vou utilizar para juntar todos os dados ao decorrer da transformação dos dados.
    ```python
    df_filme = df_tmdb.withColumn("paisOrigem", explode(split(col("paisOrigem"), ",")))
    ```
- Realizo a junção do dataframe de df_filme com o df_pais através da coluna paisOrigem. Realizei essa junção com o método `inner` pois dessa forma filtro apenas os dados que tenho os países de origem dos filmes que são dados relevantes para minha análise (apenas 5 filmes foram descartados).
    ```python
    df_filme = df_filme.join(df_pais, on="paisOrigem", how="inner")
    ```
- Renomenado a coluna paisOrigem
    ```python
    df_pais = df_pais.withColumnRenamed("paisOrigem", "pais")
    ```
- A próxima etapa do script foi criar um dataframe para armazenar as informações sobre os gêneros, que incluem o nome e o ID. A coluna de gêneros resgatada da API TMDB na etapa de ingestão de dados contém apenas os [IDs dos gêneros](Evidencias/print_dados_pais_e_genero_agrupados_como_lista.png). Esses dados foram extraídos diretamente da documentação da API TMDB. Como esses valores são fixos e há apenas 19 itens, para padronizar, decidi traduzi-los para o português.
- Obs.: Estou trabalhando com base nos gêneros da API TMDB pois muitos filmes dos arquivos CSV não são considerados do gênero de crime e guerra e no TMDB são. Evidêncio um exemplo disso na entrega da [etapa 3 na sprint 8](/Sprint%208/Desafio)
    ```python
    generos_rdd = spark.sparkContext.parallelize([\
        (28, "Ação"),\
        (12, "Aventura"),\
        (16, "Animação"),\
        (35, "Comédia"),\
        (80, "Crime"),\
        (99, "Documentário"),\
        (18, "Drama"),\
        (10751, "Família"),\
        (14, "Fantasia"),\
        (36, "História"),\
        (27, "Terror"),\
        (10402, "Música"),\
        (9648, "Mistério"),\
        (10749, "Romance"),\
        (878, "Ficção Científica"),\
        (10770, "Filme para TV"),\
        (53, "Suspense"),\
        (10752, "Guerra"),\
        (37, "Faroeste")\
    ])

    # Criando dataFrame de generos apartir do rdd
    df_generos = spark.createDataFrame(generos_rdd, ["id_genero", "genero"])
    ```
- Evidência da extração dos dados de gênero na documentação da API TMDB:
![](Evidencias/print_evidencia_resgatando_dados_de_generos_de_filmes_na_api_TMDB.png)

- Novamente usei a função ´explode()´ para dessa vez transformar a coluna 'generoTMDB' do df_filmes em múltiplas linhas, uma para cada gênero e após isso realizo a junção com o `df_genero`.
    ```python
    df_filme = df_filme.withColumn("id_genero", explode(split(col("generoTMDB"), ",")))

    df_filme = df_filme.join(df_generos, on="id_genero", how="inner")
    ```

- Após isso, selecionei dos dados do CSV apenas as colunas: id, tituloPrincipal, tituloOriginal, notaMedia e numeroVotos. As duas últimas colunas contém dados provindos da plataforma de análise de filmes IMDB. Depois elimino as linhas duplicadas e realizo a junção com o dataframe geral dos dados.
    ```python
    df_csv_filtrado = df_csv.select("id", "tituloPrincipal", "tituloOriginal", "notaMedia", "numeroVotos")

    df_csv_filtrado = df_csv_filtrado.dropDuplicates()

    df_filme = df_filme.join(df_csv_filtrado, on="id", how="inner")
    ```
- Com todos os dados já salvos, filtrados e juntados, o próximo passo foi padronizá-los.
- Primeiramente, renomeando os nomes das colunas.
    ```python
    df_filme = df_filme.withColumnRenamed("id", "id_filme")\
                        .withColumnRenamed("tituloOriginal", "titulo_original")\
                        .withColumnRenamed("tituloPrincipal", "titulo_principal")\
                        .withColumnRenamed("anoLancamentoTMDB", "ano_lancamento")\
                        .withColumnRenamed("posterLink", "poster_link")\
                        .withColumnRenamed("notaMediaTMDB", "nota_media_TMDB")\
                        .withColumnRenamed("numeroVotosTMDB", "numero_votos_TMDB")\
                        .withColumnRenamed("notaMedia", "nota_media_IMDB")\
                        .withColumnRenamed("numeroVotos", "numero_votos_IMDB")\
                        .withColumnRenamed("popularidadeTMDB", "popularidade_TMDB")

    ```
- Adicionando a base do link para ter acesso ao poster dos filmes, pois de padrão da API é retornado apenas uma parte do link que é expecífico do filme.
    ```python
    df_filme = df_filme.withColumn('poster_link', concat(lit('https://image.tmdb.org/t/p/w500'), df_filme['poster_link']))
    ```
![](Evidencias/print_evidencia_dados_coluna_posterlink_antes.png)
- Padronizando as colunas de id_genero e id_pais para o tipo integer nos dataframes que as contém.
    ```python
    df_filme = df_filme.withColumn("id_genero", col("id_genero").cast(IntegerType()))\
                    .withColumn("id_pais", col("id_pais").cast(IntegerType()))
    df_pais = df_pais.withColumn("id_pais", col("id_pais").cast(IntegerType()))
    df_generos = df_generos.withColumn("id_genero", col("id_genero").cast(IntegerType()))
    ```
- Criando o dataframe da dimensão filme conforme o modelo dimensional dos meus dados e eliminando linhas duplicadas.
    ```python
    dim_filme = df_filme.select("id_filme", "titulo_original", "titulo_principal", "poster_link", "ano_lancamento")
    dim_filme = dim_filme.dropDuplicates()
    ```
- Criando os dataframes das dimensão país e gênero
    ```python
    dim_pais = df_pais
    dim_genero = df_generos
    ```
- Criando dataframe fato filmes conforme o modelo dimensional dos meus dados.
```python
fato_filme = df_filme.select("id_filme", "id_genero", "id_pais", "orcamento", "popularidade_TMDB", "nota_media_TMDB", "numero_votos_TMDB", "nota_media_IMDB", "numero_votos_IMDB")
```
- Imprimo a quantidade de linhas e o esquema de cada dataframe dimensional
print(f"Quantidade de filmes: {dim_filme.count()}")
dim_filme.printSchema()
print(f"Quantidade de paises: {dim_pais.count()}")
dim_pais.printSchema()
print(f"Quantidade de gêneros: {dim_genero.count()}")
dim_genero.printSchema()
print(f"Quantidade de linhas da tabela fato filmes: {fato_filme.count()}")
fato_filme.printSchema()

- Por fim, salvo os dataframe dimensionais como arquivo parquet na camada Refined particionando de acordo cada dataframe.
```python
dim_filme.write.mode("overwrite").parquet(f'{S3_TARGET_PATH}/dim_filme')
dim_genero.write.mode("overwrite").parquet(f'{S3_TARGET_PATH}/dim_genero')
dim_pais.write.mode("overwrite").parquet(f'{S3_TARGET_PATH}/dim_pais')
fato_filme.write.mode("overwrite").parquet(f'{S3_TARGET_PATH}/fato_filme')

job.commit()
```

- Código completo com os devidos comentários em: [Codigos/job/job_processamento_camada_refined.py](Codigos/job/job_processamento_camada_refined.py)
- Evidência do código no ETL job:
![](Evidencias/print_evidencia_codigo_do_script_no_job_parte_1.png)
![](Evidencias/print_evidencia_codigo_do_script_no_job_parte_2.png)
![](Evidencias/print_evidencia_codigo_do_script_no_job_parte_3.png)

- Evidência do job sendo executado com sucesso:
![](Evidencias/print_evidencia_job_executado_com_sucesso.png)
- Evidência de log no ClouldWatch do job após ser executado:
  - Esquema de como os dados estavam do csv e tmdb da camada trusted:
  ![](Evidencias/print_evidencia_de_execucao_log_cloudwatch_parte_1.png)
  - Quantidade de linhas e esquema de como ficaram os dados dimensionados:
  ![](Evidencias/print_evidencia_de_execucao_log_cloudwatch_parte_2.png)
- Evidência dos dados na camada Refined no bucket s3:
![](Evidencias/print_evidencia_bucket_com_diretorio_refined.png)
![](Evidencias/print_evidencia_bucket_camada_refined_particionamentos.png)
![](Evidencias/print_evidencia_bucket_camada_refined_dimensao_filme.png)
![](Evidencias/print_evidencia_bucket_camada_refined_dimensao_genero.png)
![](Evidencias/print_evidencia_bucket_camada_refined_dimensao_pais.png)
![](Evidencias/print_evidencia_bucket_camada_refined_fato_filme.png)

### 3️⃣ Criação do Crawler
- Com os dados armazenados na camada refined o próximo passo foi criar o crawler responsável por catalogar os meus dados da camada Refined e criar as tabelas em um database a partir dos meus dados padronizados em parquet.
- Evidência de database criado nos serviços da AWS glue:
![](Evidencias/print_evidencia_database_criado.png)

- Crawler criado com as seguintes configurações:
    - Dados de origem estão apontando para o bucket s3 na camada Refined
    - Defini a IAM role AWSGlueServiceRole-DesafioFinal-Etapa3 com as políticas evidenciadas acima.
    - O database de destino é de desafio-final-filmes-modelo-dimensional evidenciado acima, agendado sob demanda.
![](Evidencias/print_evidencia_configuracao_crawler.png)
- Após a criação do crawler, foi executado o crawler criação das tabelas.
- Evidências de execução do crawler:
![](Evidencias/print_evidencia_execucao_crawler.png)
- Com a execução do crawler foram criadas quatro tabelas: Dimensão de filmes, genero, pais e a tabela fato filmes.
- Evidência das tabelas criadas no database:
![](Evidencias/print_evidencia_tabelas_criadas_no_database_apos_execucao_crawler.png)
### 4️⃣ Executando consultas no AWS Athena
- Com as tabelas multidimensionais criadas, com base nos dados da camada Refined, realizei consultas em SQL para testes da confiabilidade dos dados utilizando o serviço da AWS Athena.
- Primeiramente, tive que selecionar o banco de dados desafio-final-filmes-modelo-dimensional.
![](Evidencias/print_evidencia_tabelas_no_athena_parte_1.png)
![](Evidencias/print_evidencia_tabelas_no_athena_parte_2.png)

- Consultando todos os dados da tabela dimensão de filmes. Como resultado, obtive um total de 834 filmes, com a mesma quantidade do dataframe salvo.
![](Evidencias/print_evidencia_athena_consulta_dimensao_filmes.png)
- Consultando todos os dados da tabela dimensão de país. Como resultado, obtive um total de 60 países, com a mesma quantidade do dataframe salvo.
![](Evidencias/print_evidencia_athena_consulta_dimensao_pais.png)
- Consultando todos os dados da tabela dimensão de gênero. Como resultado, obtive um total de 19 gêneros, com a mesma quantidade do dataframe salvo.
![](Evidencias/print_evidencia_athena_consulta_dimensao_genero.png)
- Consultando todos os dados da tabela fato filmes. Como resultado, obtive um total de 3114 linhas, com a mesma quantidade do dataframe salvo.
![](Evidencias/print_evidencia_athena_consulta_fato_filme.png)

- Realizando a junção de todas as dimensões com a tabela fato:
![](Evidencias/print_evidencia_consulta_athena_juncao_de_todas_tabelas_dimensao_com_tabela_fato_parte_1.png)
![](Evidencias/print_evidencia_consulta_athena_juncao_de_todas_tabelas_dimensao_com_tabela_fato_parte_2.png)

- Consulta de soma e média de orçamento e quantidade de filmes por ano. Foi realizado uma subconsulta que faz uma média dos orçamento da tabela fato agrupados pelo id_filme para não ocorrer várias somas do orçamento do mesmo filme, visto que a tabela fato tem linhas multivaloradas de gênero e país.
![](Evidencias/print_evidencia_athena_consulta_orcamento_por_ano.png)

- Consulta da média de avaliações do TMDB, IMDB e popularidade dos filmes de crime por gêneros para se saber quais gêneros mais 'combinam' com os de crime. 
![](Evidencias/print_evidencia_consulta_media_de_avaliacoes_dos_filmes_de_crime_por_generos.png)
- ***Todas as consultas maiores em sql: [Codigos/consultas_sql/](Codigos/consultas_sql/)***

### Após analisar os dados da camada Refined e ver que estão padronizados, multidimensionados e são confiáveis, os dados estão prontos para geração de relatórios da próxima etapa do desafio final.

### Referências

- [Documentação de funções Spark Sql](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html)

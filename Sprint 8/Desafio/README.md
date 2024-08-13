# Sobre o desafio
- O desafio desta sprint é avançar para a terceira etapa do desafio final, que envolve o processamento da Camada Trusted. Nesta fase, o objetivo é assegurar que os dados sejam limpos e confiáveis, como resultado do tratamento dos dados presentes na Raw Zone.
    
## 🏆 Tema Desafio final

#### Como tema do desafio final, escolhi analisar os filmes dos gêneros crime e guerra lançados entre 2012 e 2022. O foco da análise é entender a relação entre a média de avaliação, popularidade e orçamento, a avaliação de filmes com atores conhecidos e as tendências de orçamento e popularidade.
#### Busco responder as seguintes questões: 
- Qual é a média de avaliação e a média de popularidade dos 10 filmes com os maiores orçamentos lançados entre 2012 e 2022 para cada um dos gêneros guerra e crime? Os filmes de guerra e crime analisados têm uma aceitação geral positiva de acordo com a média de popularidade para seus respectivos gêneros?  
- Qual a média de avaliação dos filmes lançados entre 2012 e 2022 para cada um dos gêneros guerra e crime que tiveram atores com mais de 3 títulos mais conhecidos?
- A média dos orçamentos para filmes dos gêneros 'guerra' e 'crime' aumentou de 2012 a 2022? E a média de popularidade desses filmes seguiu uma tendência similar durante o mesmo período?

- Para responder às minhas perguntas, obtive os seguintes dados da API TMDB durante a etapa de ingestão:
    - Orçamento;
    - Popularidade no tmdb;
    - Média de votos do TMDB;
    - Contagem de votos;
    - 5 atores principais;
    - Diretores;
    - Gênero ids;
    - Data de lançamento;
    - País de origem;
- Os dados acima vinheram na seguinte formatação json:
![](Evidencias/print_arquivo_json_parte_1.png)
![](Evidencias/print_arquivo_json_parte_2.png)
  
## 📋 Etapas

### 1️⃣ Decidir quais dados iria utilizar para minha análise

- A primeira etapa foi analisar todos os meus dados contidos na camada Raw Zone e verificar quais dados eu iria utilizar para realizar a minha análise. Após isso, percebi que nesta etapa precisaria descartar alguns dados pois não teria utilidade no foco da análise das minhas questões.
- Entre eles estão: 
    - Ano de nascimento e falecimento dos atores que estão no arquivo csv. 
    - Atores e diretores do json (Utilizarei apenas os dados de atores contidos no csv, mais precisamente da coluna `títulos mais conhecidos`).
    - Linguagem original. 
    - Mês e dia de lançamento.
- Por fim, para a minha análise será necessário apenas os dados:
  - **CSV**:
    - id;
    - Titulo principal;
    - Titulo Original;
    - Ano lançamento;
    - Tempo minutos;
    - Gênero;
    - Nota media;
    - Numero de votos;
    - Genero Artista;
    - Personagem;
    - Nome do artista;
    - Profissão;
    - Titulos do artista mais conhecidos.
  - **TMDB**:
    - Id;
    - Titulo;
    - Orçamento;
    - Popularidade;
    - Nota media;
    - Numero de votos;
    - Poster link;
    - Pais de origem;
    - Gênero;
    - Ano de Lançamento.

### 2️⃣ Criar o job para processamento dos arquivos json

- Após analisar quais dados iria trabalhar, o segundo passo foi criar o job responsável por realizar o processamento de padronização dos dados utilizando a ferramenta do AWS Glue que é o job.
- De início como iria ter acesso a outra ferramentas da AWS, criei uma IAM role com as permissões:
  - AmazonS3FullAcess;
  - AWSGlueConsoleFullAcess;
  - AWSLakeFormationAdmin;
  - CloudWatchFullAcess.
![](Evidencias/print_IAM_role.png)

- Logo após, criei o job com as seguintes configurações:
![](Evidencias/print_job_configuracao_part_1.png)
![](Evidencias/print_job_configuracao_part_2.png)
- Nos parâmetros, adicionei `S3_INPUT_PATH` com o caminho da raw zone onde estão os meus arquivos json, que estão no caminho `s3://desafio-final-filmes-e-series-anderson-neves/Raw/TMDB/JSON/Movies/`
  ![](Evidencias/print_arquivos_json_no_bucket.png)
- Adicionei também aos parâmetros `S3_TARGET_PATH` o caminho alvo onde vou exportar os meus arquivos formatados em tipos parquet, que vão ficar na camada Trusted: `s3://desafio-final-filmes-e-series-anderson-neves/Trusted/TMDB`
![](Evidencias/print_parametros_job_json.png)
- Após configurar o job, criei o script em spark para modelar os meus dados
- Primeiramente, o código mostra a importação das bibliotecas que irei utiliza
    ```python
    import sys
    from awsglue.transforms import *
    from datetime import datetime
    from awsglue.utils import getResolvedOptions
    from pyspark.context import SparkContext
    from awsglue.context import GlueContext
    from awsglue.job import Job
    from pyspark.sql.functions import col, concat_ws, round, year, trim
    from pyspark.sql.types import DoubleType, IntegerType, DecimalType
    ```
- Extrai os parâmetros que vou trabalhar e inicializei todos os contextos de trabalho com spark e o glue (configurações padrões).
    ```python
    args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH', 'S3_TARGET_PATH'])
    sc = SparkContext()
    glueContext = GlueContext(sc)
    spark = glueContext.spark_session
    job = Job(glueContext)
    job.init(args['JOB_NAME'], args)
    ```
- Defini uma variável para armazenar os caminho onde meus arquivos json estão, o diretório datado referece a última ingestão de dados realizada pela minha função lambda programada para compilar uma vez na semana, dessa forma obtenho dados atualizados.
    ```python
    source_file = args['S3_INPUT_PATH'] + '/2024/08/03/*.json'
    ```
- Recebo a data atual no formato `AAAA/MM/DD` para ser usada como particionamento dos meus dados que vão ser exportados para a camada trusted
  ```python
    current_date = datetime.now().strftime('%Y/%m/%d')
    target_path = f"{args['S3_TARGET_PATH']}/{current_date}/"
  ```

- Realizando a leitura e transformando meus dados json em data frame, tive que utilizar a opção multline pois meus dados no json continham múltiplas linhas.
  ```python
  df_movies = spark.read.option('multiline', 'true').json(source_file)
  ```
- Imprimo o esquema do dataFrame antes da formatação.
  ```python
    df_movies.printSchema()
  ```
- Seleciono apenas as colunas que vou trabalhar, descartando as outras.
  ```python
  df_movies = df_movies.select("imdb_id", "title","release_date","budget", "popularity", "vote_average", "vote_count", "poster_path" , "origin_country", "genre_ids")
  ```
- No meu json os itens país de origem(origin_country) e gênero id (genre_ids) estavam em um array, para padronizar toda coluna resolvi adicionar os seus itens na mesma linha separados por vígula, utilizando a função `concat_ws()`
  ```python
  df_movies = df_movies.withColumn("origin_country", concat_ws(",", col("origin_country")))\
                       .withColumn("genre_ids", concat_ws(",", col("genre_ids")))
  ```
- A média de votos estava vindo em alguns casos com mais de três casas decimais, então padronizei toda a coluna para apenas uma casa decimal utilizando a função `round()`.
    ```python
        df_movies = df_movies.withColumn("vote_average", round(col("vote_average"), 1))
    ```
- Como na minha análise irei trabalhar apenas com o ano de lançamento, extraí da colunas de data de lançamento apenas o ano com a função `year()`
  ```python
  df_movies = df_movies.withColumn("release_year", year(col("release_date"))).drop("release_date")
  ```
- Renomeie todas as colunas para padronizar em português
    ```python
    df_movies = df_movies.withColumnRenamed("title", "titulo") \
                                            .withColumnRenamed("budget", "orcamento") \
                                            .withColumnRenamed("poster_path", "posterLink") \
                                            .withColumnRenamed("origin_country", "paisOrigem") \
                                            .withColumnRenamed("genre_ids", "generoTMDB") \
                                            .withColumnRenamed("release_year", "anoLancamentoTMDB") \
                                            .withColumnRenamed("vote_average", "notaMediaTMDB")\
                                            .withColumnRenamed("vote_count", "numeroVotosTMDB")\
                                            .withColumnRenamed("popularity", "popularidadeTMDB")\
                                            .withColumnRenamed("imdb_id", "id")
    ```
- As colunas que continham dados que posteriomente irei realizar operações matemáticas, converti para tipos númericos utilizando a função `.cast()`. Ao transformar a coluna orçamento para o tipo Double percebi que os dados ficavam em notação científica, e como quero dados legíveis nas minhas operações de consulta, tipei para Decimal com possiveis 38 casas de valor inteiro e 2 casas decimais(pois estamos falando de valores monetários). As colunas de popularidade e média de votos não tive esse problema, então deixei como double mesmo.
    ```python
    df_movies = df_movies.withColumn("orcamento", col("orcamento").cast(DecimalType(38, 2)))\
                        .withColumn("numeroVotosTMDB", df_movies["numeroVotosTMDB"].cast(IntegerType()))\
                        .withColumn("popularidadeTMDB", df_movies["popularidadeTMDB"].cast(DoubleType()))\
                        .withColumn("notaMediaTMDB", df_movies["notaMediaTMDB"].cast(DoubleType()))
    ```

- Removi possíveis linhas das colunas principais com valores nulos e linhas duplicadas.
  ```python
  df_movies = df_movies.dropna(subset=['id','orcamento', 'numeroVotosTMDB', 'notaMediaTMDB', 'popularidadeTMDB'])

  df_movies = df_movies.dropDuplicates()
  ```
- Filtrei apenas os filmes que não continham um id do IMDB(no meu caso só foram 3 filmes) pois não iria conseguir realizar a junção porteriomente com o arquivo csv, pois esses filmes não tinha nem o nome no arquivo csv.
    ```python
    df_movies = df_movies.filter((trim(col('id')) != "") & (col('id').isNotNull()))
    ```
- Imprimo a quantidade de linhas, esquema e primeiras linhas do DataFrame que será salvo
    ```python
    print(f"quantidade de linhas: {df_movies.count()}")
    df_movies.printSchema()
    df_movies.show(truncate=False)
    ```
- Por fim, exporto o dataFrame para o tipo parquet na camada trusted no diretório TMDB, particionado pela data de processamento do job.
    ```python
    df_movies.write.mode("overwrite").parquet(target_path)

    job.commit()
    ```
- ***Código completo em: [Codigos/job_desafio_final_tmdb.py](Codigos/job_desafio_final_tmdb.py)***
- Evidencias do script:
![](Evidencias/print_job_json_script_parte_1.png)
![](Evidencias/print_job_json_script_parte_2.png)

- Evidências de execução:
![](Evidencias/print_evidencia_execucao_job_json_run_details.png)
- Evidência de output log
  - Na primeira parte está o esquema original do data frame sem o tratamento e a quantidade de linhas após o tratamento.
  ![](Evidencias/print_evidencia_de_output_log_do_job_json_parte_1.png)
  - Na segunda parte tem o esquema de como ficou o data frame após o tratamento e a impressão de algumas linhas.
  ![](Evidencias/print_evidencia_de_output_log_do_job_json_parte_2.png)



### 3️⃣ Criando job para processamento do arquivo csv
- Realizei a criação do job nos serviço AWS Glue para o processamento do csv com as mesmas configurações do job de processamento dos arquivos json.
![](Evidencias/print_configuracoes_job_csv.png)
- Como parâmetros, passei os seguintes:
  - `S3_INPUT_PATH` referenciando o arquivo cvs de filmes no caminho `s3://desafio-final-filmes-e-series-anderson-neves/Raw/File/CSV/Movies/2024/7/18/`
    ![](Evidencias/print_arquivo_csv_no_bucket.png)
  - `S3_REFERENCE_DF_PATH` referenciando o arquivo parquet salvo no último job no caminho: `s3://desafio-final-filmes-e-series-anderson-neves/Trusted/TMDB/`
  - `S3_TARGET_PATH` referencia o destino que será exportado o data frame do job na camada trusted: `s3://desafio-final-filmes-e-series-anderson-neves/Trusted/CSV`
  - Evidência:
    ![](Evidencias/print_parametros_job_csv.png)
- Após configurar o job realizei a criação do script para o processamento dos dados
- Primeiramente, no script são importado as bibliotecas que serão utilizadas: 
  ```python
    import sys
    from awsglue.transforms import *
    from awsglue.utils import getResolvedOptions
    from pyspark.context import SparkContext
    from awsglue.context import GlueContext
    from awsglue.job import Job
    from pyspark.sql.types import IntegerType, DoubleType
  ```
- Extrai os parâmetros que vou trabalhar e inicializei todas os contextos de trabalho com spark e o glue (configurações padrões).
    ```python
    args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH','S3_TARGET_PATH','S3_REFERENCE_DF_PATH'])
    sc = SparkContext()
    glueContext = GlueContext(sc)
    spark = glueContext.spark_session
    job = Job(glueContext)
    job.init(args['JOB_NAME'], args)
    ```
- Na variável source_file defino o caminho em que o arquivo csv de filmes se encontra e target_path defino o caminho onde o data frame será exportado.
    ```python
    source_file = args['S3_INPUT_PATH']
    target_path = args['S3_TARGET_PATH']
    ```
- A variável df_path_to_filter_reference referencia o caminho onde está o meus arquivos parquet do job anterior na partição que se encontra.
  ```python
  df_path_to_filter_reference = args['S3_REFERENCE_DF_PATH'] + '2024/08/11/'
  ```
- Realizo a leitura do arquivo csv transformando em dataFrame e removo as colunas que não irei utilizar.
  ```python
  df_movies_csv = spark.read.csv(source_file, header=True, inferSchema=True, sep="|")

  df_movies_csv = df_movies_csv.drop("anoNascimento", "anoFalecimento")
  ```
- Realizo a leitura dos arquivos parquets transformando em dataFrame e imprimo a quantidade de linhas, esquema e as primeiras linhas.
    ```python
    data_frame_refence = spark.read.parquet(df_path_to_filter_reference)
    print(f"quantidade de linhas: {data_frame_refence.count()}")
    data_frame_refence.printSchema()
    data_frame_refence.show(truncate=False)
    ```
- Seleciono apenas a coluna id do dataFrame que contém os filmes de guerra e crime de 2012 a 2022 extraídos da api TMDB que contém os ids dos filmes do IMDB 
    ```python
    ids_IMDB_parquet = data_frame_refence.select("id").distinct()
    ```
- Realizo uma junção do dataFrame com os dados dos filmes contidos no csv com apenas os ids dos filmes que tenho os dados extraídos do tmdb. Motivos pelos quais realizei essa filtragem:
  -  Alguns filmes do gênero crime e guerra não são considerados esse gênero no IMDB (origem dos dados do csv) e no TMDB eles são considerados, dessa forma tenho mais filmes a serem analisados.
     -  Por exemplo, o filme Dose dupla não é considerado filme de crime no IMDB e no TMDB ele é
     ![](Evidencias/print_filme_dose_dupla_imdb.png)
     ![](Evidencias/print_filme_dose_dupla_tmdb.png)
  - Outro motivo e o principal, é que os filmes provindos do json tem os dados que quero para minha análise (orçamento e popularidade) e no csv não tenho essas informações. Dessa forma, consigo filtrar somente os dados relevantes para a minha análise.
- Realizei essa junção através do método `.join` passando como parâmetro os ids dos filmes do dataFrame com dados provindos do TMDB, referenciando a junção pela coluna id do dataFRame do csv e a junção será da forma inner, ou seja, apenas os ids em comum.
    ```python
    df_filtered_movies_csv = df_movies_csv.join(ids_IMDB_parquet, on="id", how="inner")
    ```
- Converti as colunas que posteriomete vou realizar cálculos matemáticos para tipos numéricos correspondentes.
    ```python
    df_filtered_movies_csv = df_filtered_movies_csv.withColumn("anoLancamento", df_filtered_movies_csv["anoLancamento"].cast(IntegerType()))\
                                            .withColumn("notaMedia", df_filtered_movies_csv["notaMedia"].cast(DoubleType()))\
                                            .withColumn("numeroVotos", df_filtered_movies_csv["numeroVotos"].cast(IntegerType()))
    ```
- Renomeei a coluna de título principal pois estava com o nome incorreto
    ```python
    df_filtered_movies_csv = df_filtered_movies_csv.withColumnRenamed("tituloPincipal", "tituloPrincipal")
    ```
- Removendo possíveis linhas duplicadas
    ```python
    df_filtered_movies_csv= df_filtered_movies_csv.dropDuplicates()
    ```
- Imprimindo o resultado final do dataFrame a quantidade de linhas, o esquema que ficou e as primeiras linhas.
    ```python
    print(f"quantidade de linhas: {df_filtered_movies_csv.count()}")
    df_filtered_movies_csv.printSchema()
    df_filtered_movies_csv.show(truncate=False)
    ```
- Por fim, exporto o dataFrame com os dados do csv em arquivos do tipo parquet para dentro do diretório CSV na camada Trusted do bucket do meu desafio final.
    ```python
    df_filtered_movies_csv.write.mode("overwrite").parquet(target_path)

    job.commit()
    ```
- ***Código completo em: [Codigos/job_desafio_final_csv.py](Codigos/job_desafio_final_csv.py)***
- Evidência de execução do job:
![](Evidencias/print_evidencia_execucao_job_csv_details.png)
- Evidências output log no CloudWatch:
  - Na primeira parte temos a quantidade de linhas, esquema e primeiras linhas do dataFrame com os dados do TMDB:
  ![](Evidencias/print_evidencia_de_output_log_do_csv_json_parte_1.png)
  - Nessa segunda parte temos a quantidade de linhas, o esquema e algumas das primeiras linhas do dataFrame com os dados tratados do arquivo csv de filmes:
  ![](Evidencias/print_evidencia_de_output_log_do_csv_json_parte_2.png)

### 4️⃣ Evidências da camada Trusted após execução dos jobs
![](Evidencias/print_evidencia_camada_trusted_no_bucketS3.png)
![](Evidencias/print_evidencia_camada_trusted_no_bucketS3_parte_.png)
![](Evidencias/print_evidencia_camada_trusted_particao_csv.png)
![](Evidencias/print_evidencia_camada_trusted_particao_TMDB.png)

### 5️⃣ Criação do data base
- Após a limpeza e padronização dos meus dados, criei um database nos serviços da AWS glue
![](Evidencias/print_DataBase_criado.png)

### 6️⃣ Criação do Crawler
- Com o data base criado o próximo passo foi criar o crawler responsável por catalogar os meus dados da camada Trusted e criar as tabelas do meu data base a partir dos meus dados padronizados em parquet.
- Crawler criado com as seguintes configurações:
  - Dados de origem estão apontando para o bucket s3 na camada trusted
  - Define a IAM role AWSGlueServiceRole-DesafioFinal-Etapa3 com as políticas evidenciadas acima.
  - O data base de destino é de desafio-final-filmes evidenciado acima, agendado sob demanda.
![](Evidencias/print_configuracoes_crawler.png)

- Após a criação do crawler, foi executado o crawler criação das tabelas.
- Evidências de execução do crawler:
![](Evidencias/print_evidencia_execucao_crawler.png)
- Com a execução do crawler foram criadas duas tabelas CSV e TMDB com as partições de data de processamento dos dados.
![](Evidencias/print_evidencia_execucao_crawler_parte_2.png)
- Evidência das tabelas criadas no data base:
![](Evidencias/print_evidencia_tabelas_criadas_com_execucao_do_crawler.png)
### 7️⃣ Executando consultas no AWS Athena
- Com as tabelas criadas, com base nos dados da camada trusted, realizei consultas em SQL utilizando o serviço da AWS Athena.
- Primeiramente, tive que selecionar o banco de dados desafio-final-filmes e carregar as partições da tabela TMDB.
![](Evidencias/print_evidencia_athena_carregando_particoes.png)
- Consultando todos os dados da tabela TMDB
```sql
select * from tmdb;
```
- Como resultado, obteve um total de 860 linhas, com a mesma quantidade do dataframe importado.
![](Evidencias/print_evidencia_athena_consultando_todos_os_dados_tmdb.png)
- Exibindo todos os dados da tabela CSV
```sql
select * from csv;
```
- Como resultado, obteve um total de 3378 linhas, com a mesma quantidade do dataframe importado.
![](Evidencias/print_evidencia_athena_consultando_todos_os_dados_csv.png)
- Consultando se há dados duplicados no tmdb
    ```sql
    SELECT t.*
    FROM tmdb t
    JOIN (
        SELECT id
        FROM tmdb
        GROUP BY id
        HAVING COUNT(id) > 1
    ) duplicadas ON t.id = duplicadas.id
    ORDER BY t.id
    ```
    ![](Evidencias/print_evidencia_athena_consultando_ids_duplicados_tmdb.png)
- Realizando junção das duas tabelas
    ```sql
    select * from tmdb join csv on tmdb.id = csv.id;
    ```
    ![](Evidencias/print_evidencia_athena_realizando_juncao_nas_duas_tabelas_parte_1.png)
    ![](Evidencias/print_evidencia_athena_realizando_juncao_nas_duas_tabelas_parte_2.png)
    ![](Evidencias/print_evidencia_athena_realizando_juncao_nas_duas_tabelas_parte_3.png)
    ![](Evidencias/print_evidencia_athena_realizando_juncao_nas_duas_tabelas_parte_4.png)
- Somando toda a coluna orçamento
    ```sql
    select sum(orcamento) orcamento_total count(*) quantidade_linhas from tmdb;
    ```
    ![](Evidencias/print_evidencia_athena_soma_da_coluna_orcamento.png)

- ***Todas as consultas em sql: [Codigos/consultas.sql](Codigos/consultas.sql)***

### Após analisar os dados da camada Trusted e ver que estão padronizados e são confiáveis, os dados estão prontos para ir para próxima etapa do desafio final.

### Referências

- [Documentação de funções Spark Sql](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html)

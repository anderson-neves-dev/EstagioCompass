import sys
from awsglue.transforms import *
from datetime import datetime
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, concat_ws, round, year, trim
from pyspark.sql.types import DoubleType, IntegerType, DecimalType


## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH', 'S3_TARGET_PATH'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Caminho onde estão os arquivos jsons que serão importados
source_file = args['S3_INPUT_PATH'] + '/2024/08/03/*.json'

# Salvando data atual do processamento no padrão AAAA/MM/DD
current_date = datetime.now().strftime('%Y/%m/%d')

# Caminho alvo onde será armazenado os arquivos parquet reparticionados pela data de processamento
target_path = f"{args['S3_TARGET_PATH']}/{current_date}/"

# Fazendo a leitura dos arquivos JSON de filmes no S3
df_movies = spark.read.option('multiline', 'true').json(source_file)

# Imprimindo esquema original
df_movies.printSchema()

# Selecionando apenas as colunas desejadas
df_movies = df_movies.select("imdb_id", "title","release_date","budget", "popularity", "vote_average", "vote_count", "poster_path" , "origin_country", "genre_ids")

# Convertendo tipos arrays para mesma linha separando por vírgula 
df_movies = df_movies.withColumn("origin_country", concat_ws(",", col("origin_country")))\
                     .withColumn("genre_ids", concat_ws(",", col("genre_ids")))

# Padronizando os dados de media de votos para uma casa decimal
df_movies = df_movies.withColumn("vote_average", round(col("vote_average"), 1))

# Filtrando apenas o ano da data de lançamento dos filmes
df_movies = df_movies.withColumn("release_year", year(col("release_date"))).drop("release_date")
                                                    
# Renomeando as colunas para padronizar em português
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

# Convertendo colunas que realizarão operações matemáticas para tipos numéricos               
df_movies = df_movies.withColumn("orcamento", col("orcamento").cast(DecimalType(38, 2)))\
                     .withColumn("numeroVotosTMDB", df_movies["numeroVotosTMDB"].cast(IntegerType()))\
                     .withColumn("popularidadeTMDB", df_movies["popularidadeTMDB"].cast(DoubleType()))\
                     .withColumn("notaMediaTMDB", df_movies["notaMediaTMDB"].cast(DoubleType()))

# Removendo linhas que possuem valores Nan
df_movies = df_movies.dropna(subset=['id','orcamento', 'numeroVotosTMDB', 'notaMediaTMDB', 'popularidadeTMDB'])

# Removendo linhas duplicadas
df_movies = df_movies.dropDuplicates()

# Removendo linhas da coluna id que não tenha valores
df_movies = df_movies.filter((trim(col('id')) != "") & (col('id').isNotNull()))

# Imprimindo a quantidade de linhas, esquema e primeiras linhas do DataFrame que será salvo
print(f"quantidade de linhas: {df_movies.count()}")
df_movies.printSchema()
df_movies.show(truncate=False)

# Exportando o dataFrame para o tipo parquet para a camada TRUSTED/TMDB/AAAA/MM/DD
df_movies.write.mode("overwrite").parquet(target_path)

job.commit()

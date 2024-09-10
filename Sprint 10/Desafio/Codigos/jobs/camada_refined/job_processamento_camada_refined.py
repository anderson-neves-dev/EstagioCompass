import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import split, explode, col, monotonically_increasing_id, concat, lit
from pyspark.sql.types import IntegerType


## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_CSV_PATH','S3_INPUT_TMDB_PATH', 'S3_TARGET_PATH'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Caminho dos arquivos parquet que estão na camdada Trusted
S3_INPUT_CSV_PATH = args['S3_INPUT_CSV_PATH']
S3_INPUT_TMDB_PATH = args['S3_INPUT_TMDB_PATH'] + '/2024/09/06/'

# Caminho para a camada Refined
S3_TARGET_PATH = args['S3_TARGET_PATH']

# Lendo os arquivos parquet da camada trusted e transformando em dataFrames 
df_csv = spark.read.parquet(S3_INPUT_CSV_PATH)
df_tmdb = spark.read.parquet(S3_INPUT_TMDB_PATH)

#Imprimindo o esquema dos df importados da camada trusted
df_csv.printSchema()
df_tmdb.printSchema()


# Criando RDD com os ids dos generos e seus respectivos nomes
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

# Transformando a coluna 'generoTMDB' em múltiplas linhas, uma para cada gênero
df_filme = df_tmdb.withColumn("id_genero", explode(split(col("generoTMDB"), ",")))

# Junção interna entre df_filme e df_generos pela chave 'id_genero', restringindo a registros com IDs de gênero iguais.
df_filme = df_filme.join(df_generos, on="id_genero", how="inner")

# Selecionando do arquivo csv apenas os dados que vão ser utilizaveis 
df_csv_filtrado = df_csv.select("id", "tituloPrincipal", "tituloOriginal", "notaMedia", "numeroVotos")

# Removendo linhas duplicadas
df_csv_filtrado = df_csv_filtrado.dropDuplicates()

# Junção interna entre df_filme e df_csv_filtrado pela chave 'id' dos filmes, restringindo a registros com IDs de filmes iguais.
df_filme = df_filme.join(df_csv_filtrado, on="id", how="inner")

# Renomenado colunas
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

#Adicionando a url base para acessar o posters dos filmes
df_filme = df_filme.withColumn('poster_link', concat(lit('https://image.tmdb.org/t/p/w500'), df_filme['poster_link']))

# Padronizando as colunas de ids para o tipo integer
df_filme = df_filme.withColumn("id_genero", col("id_genero").cast(IntegerType()))
df_generos = df_generos.withColumn("id_genero", col("id_genero").cast(IntegerType()))

# Criando o dataframe da dimensao filme
dim_filme = df_filme.select("id_filme", "titulo_original", "titulo_principal", "poster_link", "ano_lancamento")
dim_filme = dim_filme.dropDuplicates()

# Criando o data frame da dimensao pais e genero
dim_genero = df_generos

# Criando dataframe fato filmes
fato_filme = df_filme.select("id_filme", "id_genero", "orcamento","receita", "popularidade_TMDB", "nota_media_TMDB", "numero_votos_TMDB", "nota_media_IMDB", "numero_votos_IMDB")

# Imprindo a quantidade de linhas e o esquema de cada dataframe dimensional
print(f"Quantidade de filmes: {dim_filme.count()}")
dim_filme.printSchema()
print(f"Quantidade de gêneros: {dim_genero.count()}")
dim_genero.printSchema()
print(f"Quantidade de linhas da tabela fato filmes: {fato_filme.count()}")
fato_filme.printSchema()

# Salvando os dataframe dimensionais como arquivo parquet na camada Refined
dim_filme.write.mode("overwrite").parquet(f'{S3_TARGET_PATH}/dim_filme')
dim_genero.write.mode("overwrite").parquet(f'{S3_TARGET_PATH}/dim_genero')
fato_filme.write.mode("overwrite").parquet(f'{S3_TARGET_PATH}/fato_filme')

job.commit()

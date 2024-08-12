import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.types import IntegerType, DoubleType


## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH','S3_TARGET_PATH','S3_REFERENCE_DF_PATH'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Caminho do arquivo csv de filmes
source_file = args['S3_INPUT_PATH']
# Caminho de destino para salvar os arquivos parquet
target_path = args['S3_TARGET_PATH']
# Caminho que está o dataFrame com os dados dos filmes de guerra e crime de 2012 a 2022
df_path_to_filter_reference = args['S3_REFERENCE_DF_PATH'] + '2024/08/11/'


# Lendo o arquivo CSV
df_movies_csv = spark.read.csv(source_file, header=True, inferSchema=True, sep="|")

# Removendo colunas que não cão ser utilizadas
df_movies_csv = df_movies_csv.drop("anoNascimento", "anoFalecimento")

# Lendo os arquivos Parquet e transformando em DataFrame
data_frame_refence = spark.read.parquet(df_path_to_filter_reference)

# Imprimindo a quantidade de linhas, esquema e primeiras linhas do DataFrame que será utilizando como referencia para filtragem dos filmes de guerra e crime entre 2012 a 2022
print(f"quantidade de linhas: {data_frame_refence.count()}")
data_frame_refence.printSchema()
data_frame_refence.show(truncate=False)

# Selecionando apenas os ids imdb do dataFrame de referencia
ids_IMDB_parquet = data_frame_refence.select("id").distinct()

# Filtrando o DataFrame CSV através dos IDs do dataFrame de referência
df_filtered_movies_csv = df_movies_csv.join(ids_IMDB_parquet, on="id", how="inner")

# Convertendo as tipagens das colunas que vão realializar calculos matemáticos para tipos num´
df_filtered_movies_csv = df_filtered_movies_csv.withColumn("anoLancamento", df_filtered_movies_csv["anoLancamento"].cast(IntegerType()))\
                                         .withColumn("notaMedia", df_filtered_movies_csv["notaMedia"].cast(DoubleType()))\
                                         .withColumn("numeroVotos", df_filtered_movies_csv["numeroVotos"].cast(IntegerType()))
             
# Renomeando coluna que estava com nome incorreto                            
df_filtered_movies_csv = df_filtered_movies_csv.withColumnRenamed("tituloPincipal", "tituloPrincipal")

# Removendo linhas duplicadas
df_filtered_movies_csv= df_filtered_movies_csv.dropDuplicates()

# Imprimindo a quantidade de linhas, esquema e primeiras linhas do DataFrame que será salvo
print(f"quantidade de linhas: {df_filtered_movies_csv.count()}")
df_filtered_movies_csv.printSchema()
df_filtered_movies_csv.show(truncate=False)

# Exportando o dataFrame para o tipo parquet para a camada TRUSTED/CSV
df_filtered_movies_csv.write.mode("overwrite").parquet(target_path)

job.commit()

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, upper, count, max

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH', 'S3_TARGET_PATH'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

source_file = args['S3_INPUT_PATH']
target_path = args['S3_TARGET_PATH'] + '/frequencia_registro_nomes_eua'

# Fazendo a leitura do arquivo csv nomes que está no meu bucket s3 passado na variavel de parametro S3_INPUT_PATH
data_frame_com_arquivo_nomes = spark.read.option("header", True).option("sep", ",").csv(source_file)

# Imprimo somente o schema  para ver as tipagens de cada coluna
data_frame_com_arquivo_nomes.printSchema()

# Convertendo para maiúculo os nomes que estão na coluna nomes
data_frame_com_arquivo_nomes = data_frame_com_arquivo_nomes.withColumn("nome", upper(col("nome")))

# Imprindo a contagem de linhas que o arquivo possui
print(f"Total de linhas: {data_frame_com_arquivo_nomes.count()}")

# Imprimindo a contagem de nomes, agrupando os dados pelas colunas ano e sexo, e ordenando pela coluna ano de forma decrescente para pegar os anos mais recentes
contagem_dos_nomes = data_frame_com_arquivo_nomes.groupBy("ano", "sexo").count().orderBy(col("ano").desc())
contagem_dos_nomes.show()

# Ordenando o data frame principal de forma decrescente pela coluna ano 
data_frame_com_arquivo_nomes = data_frame_com_arquivo_nomes.orderBy(col("ano").desc())

# Imprindo o nome feminino com mais registros e o ano que ocorreu
nome_feminino_com_mais_registros = data_frame_com_arquivo_nomes.filter(col("sexo") == "F").groupBy("nome", "ano").agg(max("total").alias("max_total")).orderBy(col("max_total").desc()).first()
print(f"Nome feminino com mais registros: {nome_feminino_com_mais_registros['nome']} em {nome_feminino_com_mais_registros['ano']}")

# Imprindo o nome masculino com mais registros e o ano que ocorreu
nome_masculino_com_mais_registros = data_frame_com_arquivo_nomes.filter(col("sexo") == "M").groupBy("nome", "ano").agg(max("total").alias("max_total")).orderBy(col("max_total").desc()).first()
print(f"Nome masculino com mais registros: {nome_masculino_com_mais_registros['nome']} em {nome_masculino_com_mais_registros['ano']}")

# Imprimindo o agrupamento do total de registros masculinos e femininos para cada ano
total_registros_por_ano = data_frame_com_arquivo_nomes.groupBy("ano").agg(count("nome").alias("total_registros"))
total_registros_por_ano.show()

# Extraindo apenas as 10 primeras linhas ordenadas pelo ano de forma crescente
filtragem_primeiras_10_linhas = data_frame_com_arquivo_nomes.orderBy(col("ano").asc()).limit(10)
filtragem_primeiras_10_linhas.show()

# Exportando em formato json os conteúdos do dataframe com o particionamentona ordem sexo e ano para o diretorio target no meu bucket s3 
data_frame_com_arquivo_nomes.write.partitionBy("sexo", "ano").json(target_path)

job.commit()
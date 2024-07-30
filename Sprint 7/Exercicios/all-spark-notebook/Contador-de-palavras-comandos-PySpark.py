#Importando Biblioteca SparkSession
from pyspark.sql import SparkSession

# Iniciando uma sSparkSession
spark = SparkSession.builder.appName("ContadorDePalavrasReadme").getOrCreate()
spark_context = spark.sparkContext

# Lendo o arquico README.md que está no container docker
arquivo_readme = sc.textFile('README.md')

# Testando para ver se conseguiu ler e imprimir a quantidade de linhas no arquivo
print(arquivo_readme.count())

# importando a biblioteca re
import re

# Extraindo das linhas todas as palavras 
palavras = arquivo_readme.flatMap(lambda linha: re.split('\W+', linha.lower().strip()))

# Mapeando o rdd para cada palavra adicionar a quantidade de 1 em outra coluna
palavras = palavras.map(lambda palavra: (palavra,1))

# Importando add
from operator import add

# Mesclando o rdd para contar a quantidade que cada palavra se repete
palavras = palavras.reduceByKey(add)

# Exibindo a coleção
palavras.collect()

# Filtrando apenas as palavras 
palavras = palavras.filter(lambda palavra: palavra[0].strip() != '')

# Ordenando de forma decrecente pela quantidade
palavras_ordenadas = palavras.sortBy(lambda palavra: palavra[1], ascending=False)

# Exibindo a coleção ordenada
palavras_ordenadas.collect()

# Criando um data frame com o schema de colunas
palavras_ordenadas_df = spark.createDataFrame(palavras_ordenadas, ["Palavra", "Quantidade"])

# Exportando o data frame com tipo parquet para dentro do container
palavras_ordenadas_df.write.parquet("/home/jovyan/palavras_ordenadas_df.parquet")

# Exibindo o Data Frame
palavras_ordenadas_df.show()

# Encerrando a sessão spark
spark.stop()
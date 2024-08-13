# Etapa 1
from pyspark.sql import SparkSession
from pyspark import SparkContext, SQLContext, SparkConf
from pyspark.sql.functions import when, rand, col, floor
from pyspark.sql.types import IntegerType

# Configurando para não exibir logs
spark_configuracao = SparkConf().set("spark.eventLog.enabled", "false")

# Cria a SparkSession
spark = SparkSession \
    .builder \
    .master("local[*]") \
    .appName("Exercicio Intro") \
    .config(conf=spark_configuracao)\
    .getOrCreate()

# Ajusta o nível de log para aprecer somente os logs WARN 
spark.sparkContext.setLogLevel("WARN")

# Lendo o arquivo txt e transformando em um dataFrame
df_nomes = spark.read.csv("nomes_aleatorios.txt")
print("\n\n\n\n\n Primeiras 5 linhas do data frame")
df_nomes.show(5)

# Etapa 2

print("\n\n\n\n\n Esquema do data frame após o renomeio da coluna para Nomes")
# Renomeando a coluna para Nomes
df_nomes = df_nomes.withColumnRenamed("_c0", "Nomes")
df_nomes.printSchema()

#Etapa 3

#Criando a coluna de Escolaridade com valores aleatorios
df_nomes = df_nomes.withColumn(
    "Escolaridade",
    when(rand() < 0.33, "Fundamental")
    .when((rand() >= 0.33) & (rand() < 0.66), "Medio")
    .otherwise("Superior")
)
print("\n\n\n\n\n Data frame com coluna de Escolaridade")
df_nomes.show(5)

# Etapa 4

#Criando a coluna de Pais com valores aleatorios
df_nomes = df_nomes.withColumn(
    "Pais",
    when(rand() < 0.07, "Brasil")
    .when((rand() >= 0.07) & (rand() < 0.15), "Argentina")
    .when((rand() >= 0.15) & (rand() < 0.23), "Bolivia")
    .when((rand() >= 0.23) & (rand() < 0.30), "Peru")
    .when((rand() >= 0.30) & (rand() < 0.38), "Uruguay")
    .when((rand() >= 0.38) & (rand() < 0.46), "Chile")
    .when((rand() >= 0.46) & (rand() < 0.53), "Venezuela")
    .when((rand() >= 0.53) & (rand() < 0.61), "Colombia")
    .when((rand() >= 0.61) & (rand() < 0.69), "Paraguai")
    .when((rand() >= 0.69) & (rand() < 0.76), "Equador")
    .when((rand() >= 0.76) & (rand() < 0.84), "Suriname")
    .when((rand() >= 0.84) & (rand() < 0.92), "Guiana")
    .otherwise("Guiana Francesa")
)

print("\n\n\n\n\n Data frame com coluna de Pais")
df_nomes.show(5)

#Etapa 5

# Criando a coluna AnoNascimento com valores aleatórios entre 1945 e 2010
df_nomes = df_nomes.withColumn(
    "AnoNascimento",
    (floor(rand() * (2010 - 1945 + 1)) + 1945).cast(IntegerType())
)

print("\n\n\n\n\n Data frame com coluna de AnoNascimento")
df_nomes.show(5)

# Etapa 6

# Selecionando apenas os nomes das pessoas que nasceram no século atual
df_select =  df_nomes.select("Nomes").filter((col("AnoNascimento") >= 2001))
print("\n\n\n\n\n Nomes das pessoas que nasceram no século atual")
df_select.show(10)

# Etapa 7

# Registrando uma tabela temporária com o nomes Pessoas
df_nomes.createOrReplaceTempView("Pessoas")

print("\n\n\n\n\n Nomes das pessoas que nasceram no século atual usando spark SQL")

# Selecionando apenas os nomes das pessoas que nasceram no século atual com Spark SQL
spark.sql("select nomes from pessoas where AnoNascimento >= 2001").show()


# Etapa 8

# Selecionando  e realizando a contagem apenas os nomes das pessoas do século Millennials
print("\n\n\n\n\n Quantidade de pessoas da geração Millennials")
df_millennials = df_nomes.filter((col("AnoNascimento") >= 1980) & (col("AnoNascimento") <= 1994))

print(df_millennials.count())

# Etapa 9

print("\n\n\n\n\n Quantidade de pessoas da geração Millennials usando Spark SQL")

# Selecionando apenas os nomes das pessoas do século Millennials com Spark SQL
spark.sql("select count(*) as Numero_de_pessoas_da_geracao_milenar from pessoas where AnoNascimento BETWEEN 1980 and 1994").show()

#Etapa 10

# Quantidade de pessoas de cada país para cada geração com o uso de Spark SQL
df_result = spark.sql("""
    SELECT 
        Pais, 
        Geracao, 
        COUNT(*) as Quantidade
    FROM 
        (
            SELECT 
                Pais,
                CASE
                    WHEN AnoNascimento BETWEEN 1944 AND 1964 THEN 'Baby Boomers'
                    WHEN AnoNascimento BETWEEN 1965 AND 1979 THEN 'Geração X'
                    WHEN AnoNascimento BETWEEN 1980 AND 1994 THEN 'Millennials'
                    WHEN AnoNascimento BETWEEN 1995 AND 2015 THEN 'Geração Z'
                END AS Geracao
            FROM Pessoas
        ) AS tabelaComColunaGeracao
    GROUP BY 
        Pais, Geracao
""")

# Ordenando o DataFrame pelos campos Pais, Geracao e Quantidade
df_ordered_result = df_result.orderBy("Pais", "Geracao", "Quantidade")
print("\n\n\n\n\n Quantidade de pessoas de cada país para cada geração:")
df_ordered_result.show(10)

spark.stop()

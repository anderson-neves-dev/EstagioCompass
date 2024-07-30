# Aprendizagens 
# 📝 Exercício

## 1️⃣ Apache Spark - Contador de Palavras
- Etapa 1: Baixar a imagem jupyter/all-spark-notebook.
- Comando:
    ```
    docker pull jupter/all-spark-notebook
    ```
- Etapa 2: Criar container e rodar de forma interativa usando a imagem jupter/all-spark-notebook na porta 8888, nomeando o container `spark_jupyter` e removendo após execução  
    ```
    docker run -it --rm --name spark_jupyter -p 8888:8888 jupyter/all-spark-notebook
    ```
    ![](Evidencias/print_exSpark_executando_container_de_forma_interativa_com_imagem_jupter_spark_na_porta_8888.png)
    ![](Evidencias/print_exSpark_Jupyter_na_porta_local_8888.png)

- Etapa 3: Iniciando uma sessão interativa do PySpark com o comando `pyspark` no container spark_jupyter utilizando comando docker `exec` e `-i -t` para rodar de forma interativa dentro do container.
    ```
    docker exec -i -t spark_jupyter pyspark
    ```
    ![](Evidencias/print_exSpark_terminal_iniciando_pyspark_no_container_spark_jupyter.png)
- Etapa 4: Em outro terminal fiz o dowload do meu README principal do diretório onde estão meus dados da compass. Gerei um token no meu github para consegui realizar dowload com `wget` e utilizei o comando `exec` para executar dentro do container docker.
    ```
    docker exec spark_jupyter wget -c --header="Authorization: token token_de_acesso" https://raw.githubusercontent.com/anderson-neves-dev/EstagioCompass/main/README.md
    ```
    ![](Evidencias/print_exSpark_download_readme_com_wget_para_dentro_do_container_spark_jupyter.png)
    ![](Evidencias/print_exSpark_Arquivo_README_no_container.png)

- Etapa 5: Realizando a contagem e palavras do arquivo README dentro da sessão PySpark
  - 
    ```python
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
    ```
- Evidências de execução dos comando acima
    ![](Evidencias/print_exSpark_terminal_spark.png)
    ![](Evidencias/print_exSpark_terminal_spark_parte_2.png)
- Etapa 6: Resgatar os dados Parket no jupyter e criar um gráfico com matploplib
    ![](Evidencias/print_exSpark_trabalhando_com_os_dados_parket_no_Jupyter_part_1.png)
    ![](Evidencias/print_exSpark_trabalhando_com_os_dados_parket_no_Jupyter_part_2.png)
    ![](Evidencias/print_exSpark_trabalhando_com_os_dados_parket_no_Jupyter_part_3.png)
  
- Explicação do código no jupyter bem como os resutados em:  [Exercicios/all-spark-notebook/exSpark.ipynb](Exercicios/all-spark-notebook/exSpark.ipynb)

## 2️⃣ Lab AWS Glue

- Etapa 1: Configurar Athena

- Etapa 2: Criar um banco de dados

# 🏆 Certificados


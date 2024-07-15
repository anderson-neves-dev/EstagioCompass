# 📝 Exercício

## 1️⃣ Lab AWS S3
- Etapa 1: Criar um bucket

<img src="Evidencias/bucket-criado.png" width="80%">

- Etapa 2: Habilitar hospedagem de site estático
<img src="Evidencias/personalizando-habilitacao-site-estatico.png" width="80%">

- Etapa 3: editar as configurações do Bloqueio de acesso público
<img src="Evidencias/retirando-bloqueio-de-acesso-publico.png" width="80%">

- Etapa 4: Adicionar política de bucket que torna o conteúdo do bucket publicamente disponível
<img src="Evidencias/personalizando-permissoes.png" width="80%">

- Etapa 5: Configurar um documento de índice
  - Arquivo indice: [index.html](Exercicios/Lab-aws-S3/index.html)
- Etapa 6: configurar documento de erros
    - Arquivo indice: [error.html](Exercicios/Lab-aws-S3/error.html)
  - Aquivos index.html e error.html armazenados no bucket s3
  <img src="Evidencias/bucket-com-os-arquivos-html.png" width="80%">

- Etapa 7: testar o endpoint do site
  <img src="Evidencias/site-hospedado.png" width="80%">
## 2️⃣ Lab AWS Athena

- Etapa 1: Configurar Athena
  <img src="Evidencias/destinatorio-das-consultas-athena-configurado.png" width="80%">
- Etapa 2: Criar um banco de dados
  <img src="Evidencias/destinatorio-das-consultas-athena-configurado.png" width="80%">
- Etapa 3: Criar uma tabela
    -Query para criar o banco de dados:
    ```
    CREATE EXTERNAL TABLE IF NOT EXISTS meubanco.total_nomes (
        nome STRING,
        sexo STRING,
        total INT,
        ano INT
    ) 
    ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
    WITH SERDEPROPERTIES (
    'serialization.format' = ',',
    'field.delim' = ','
    )
    LOCATION 's3://exerciciosprint6.com/dados/' 
    ```
    - Executando:
  
    <img src="Evidencias/tabela-total-nomes-criada-com-sucesso.png" width="80%">

    - Testando os dados:
  
    <img src="Evidencias/resultado-teste-athena-tabela-total-nomes.png" width="80%">
    
    - Consulta que lista os 3 nomes mais usados em cada década desde o 1950 até hoje:
    - Para realizar essa consulta tive que fazer tabelas temporárias para conseguir chegar no resultado esperado
    - A primeira tabela temporária que criei foi a `MeuBancoComColunaDeDecadas`
      - Nessa tabela adicione todas as colunas que tinham na tabela `total_nomes` no banco de dados `meubanco` e adicionei a coluna decada.
      - Na coluna decada fiz um calculo para pegar a coluna ano e deicar apenas o ano da decada, ou seja, se o ano é 1952 ficará 1950 na coluna decada. Utilizei a função `FLOR()` para retirar os valores decimais do resultado da conta `ano / 10` em que vai quebrar uma casa decimal do ano `(ex.: 1983 / 10 = 198.3. FLOR(198.3 = 198))` e após a realização da função, multipliquei por 10 para ficar somente a decada `(ex: 198 * 10 = 1983)`;
      - Por ultimo faço um `WHERE ano >= 1950` para filtrar apenas os anos a partir de 1950.
      - Tabela temporária MeuBancoComColunaDeDecadas:
        ```
        WITH MeuBancoComColunaDeDecadas AS (
        SELECT nome,
            sexo,
            total,
            ano,
            (FLOOR(ano / 10) * 10) AS decada
        FROM meubanco.total_nomes
        WHERE ano >= 1950
        ),
        ```
    - Após a criação da tabela temporária acima, foi necessário criar mais outra tabela temporária para fazer o ranking dos nomes 
    - `ROW_NUMBER()`: Função de janela para atribuir um número único a cada linha dentro da partição dos resultados.
    - `OVER`: Define a janela de linhas sobre as quais a função de janela opera.
    - `PARTITION BY decada`: Divide o conjunto de resultados em partições com base no valor da coluna decada. Cada partição corresponde a uma década diferente.
    - `ORDER BY total DESC`: Dentro de cada partição (década), as linhas são ordenadas em ordem decrescente com base no valor da coluna total. Dessa forma será feito o ranking pelas decadas.
    - `FROM MeuBancoComColunaDeDecadas` por ultimo, faço tudo isso acima pela tabela temporária MeuBancoComColunaDeDecadas.

    - Tabela temporária RankingDeNomesPorDecada:

    ```
    RankingDeNomesPorDecada AS (
        SELECT nome,
            sexo,
            total,
            decada,
            ROW_NUMBER() OVER (
                PARTITION BY decada
                ORDER BY total DESC
            ) AS rankOrdenadoDeNomes
        FROM MeuBancoComColunaDeDecadas
    )
    ```
    - Por ultimo, faço a seleção de nome, sexo, total pegando da tabela temporária RankingDeNomesPorDecada fazendo uma filtragem utilizando WHERE dos números maiores ou iguais a 3 da coluna rankOrdenadoDeNomes ordeno de forma crescente utilizando ORDER BY primeiramente pela coluna decada e depois pela coluna rankOrdenadoDeNomes em que vai me dar em ordem o top 3 total de nomes por decada.
    ```
    SELECT decada,
        nome,
        sexo,
        total
    FROM RankingDeNomesPorDecada
    WHERE rankOrdenadoDeNomes <= 3
    ORDER BY decada,
        rankOrdenadoDeNomes;
    ```
    - Query completa:
    ```
    WITH MeuBancoComColunaDeDecadas AS (
    SELECT nome,
            sexo,
            total,
            ano,
            (FLOOR(ano / 10) * 10) AS decada
        FROM meubanco.total_nomes
        WHERE ano >= 1950
    ),
    RankingDeNomesPorDecada AS (
        SELECT nome,
            sexo,
            total,
            decada,
            ROW_NUMBER() OVER (
                PARTITION BY decada
                ORDER BY total DESC
            ) AS rankOrdenadoDeNomes
        FROM MeuBancoComColunaDeDecadas
    )
    SELECT decada,
        nome,
        sexo,
        total
    FROM RankingDeNomesPorDecada
    WHERE rankOrdenadoDeNomes <= 3
    ORDER BY decada,
        rankOrdenadoDeNomes;
    ```
    - Resultado da query:
    <img src="Evidencias/resultado-query-top-3-total-por-decada-apartir-1953.png" width="80%">

## 3️⃣ Lab AWS Lambda
- Etapa 1: Criar a função do Lambda
  - Obs.: Utilizei o python 3.9 que é a versão mais atual 
    <img src="Evidencias/funcao-lambda-criada.png" width="80%">
- Etapa 2: Construir o código
    <img src="Evidencias/criando-codigo-no-lamda.png" width="80%">
- Etapa 3: Criar uma Layer
    - Tive que realizar modificação: `FROM amazonlinux:latest` para pegar a ultima versão de imagem de base do amazonlinux e `RUN python3 -m pip install --upgrade --ignore-installed pip` em que rodo como o comando python3 e ignorando a instalação do pip.
    - Código Dockfile:
    ```
    FROM amazonlinux:latest
    RUN yum update -y
    RUN yum install -y \
        python3 \
        python3-pip \
        zip
    RUN yum -y clean all
    RUN python3 -m pip install --upgrade --ignore-installed pip
    ```
    - Codigo no terminal par criar a imagem acima
    ```
    docker build -t amazonlinuxpython39 .
    ```
    - Codigo no terminal para rodar o container em bash:
    ```
    docker run -it amazonlinuxpython39 bash
    ```
    - Evidencias do resto das etapas sugeridas:
    - Criando imagem:
    <img src="Evidencias/bash-criando-imagem.png" width="80%">
    - Criando os diretórios em bash no container com a imgem criada:
    <img src="Evidencias/bash-criando-diretorios.png" width="80%">
    - Instalando a biblioteca pandas:
    <img src="Evidencias/bash-instalando-pandas.png" width="80%">
    - Zipando os arquivos em bash:
    <img src="Evidencias/bash-zipando-arquivos.png" width="80%">
    <img src="Evidencias/bash-arquivos-zipados-sucesso.png" width="80%">
    - Copiando os arquivos zipados do container para o diretório local: 
    <img src="Evidencias/bash-copiando-arquivo-zipado-do-container.png" width="80%">
    - Bucket s3 com o arquivo zipado armazenado:]
    <img src="Evidencias/bucket-s3-com-biblioteca-pandas.png" width="80%"> 
- Tive alguns erros, a função lamda estava configurada para ter um timeout de busca de apensas 3 segundos e apenas 128 MB de consulta. Então, alterei para no 3 minutos e coloquei ate 256 bytes:
    <img src="Evidencias/configurando-consulta-lambda.png" width="80%"> 
- Execução da função lambda:
     <img src="Evidencias/lamba-funcao-executada-com-sucesso.png" width="80%"> 
  

# 🏆 Certificados
- Fundamentals of Analytics on AWS – Part 1 (Portugues)
  
    <img src="Certificados/fundamentos-de-anality-parte-1.jpeg" width="400">

- Fundamentals of Analytics on AWS – Part 2 (Portugues)
  
    <img src="Certificados/fundamentos-de-anality-parte-2.jpeg" width="400">

- Serverless Analytics
  
    <img src="Certificados/serveless-anality.jpeg" width="400">

- Introduction to Amazon Athena
  
    <img src="Certificados/introducao-ao-aws-athena.jpeg" width="400">

- AWS Glue Getting Stated
  
    <img src="Certificados/aws-glue-staled.jpeg" width="400">

- Amazon EMR Getting Started

    <img src="Certificados/amazon-emr.jpeg" width="400">

- Amazon Redshirt Getting Started
  
    <img src="Certificados/amazon-redshirt.jpeg" width="400">

- Best Practies for Data Warehousing with Amazon Redshirt
  
    <img src="Certificados/warehouse-with-redshirt-pratict.jpeg" width="400">

- Amazon QuickSight

    <img src="Certificados/amazon-quicksight.jpeg" width="400">


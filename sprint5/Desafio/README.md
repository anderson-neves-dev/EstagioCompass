# 📋 Etapas

## 1️⃣ Baixar uma base de dados no portal de dados públicos do Governo Brasileiro 

- A base de dados escolhida foi `Demonstrativos de Acidentes - RIOSP` que corresponde aos acidentes realizados nas rodovias de ligamento das cidades de São Paulo ao Rio de Janeiro entre março de 2022 e maio de 2024, a obtenção desses dados foi realizada pela Agência Nacional de Transportes Terrestres, entre que está disponível no link abaixo:
- [Demonstrativos de Acidentes - RIOSP](https://dados.gov.br/dados/conjuntos-dados/acidentes-rodovias)

## 2️⃣ Análise e tratamento da base de dados em .csv

- Após escolher a base de dados, fiz um estudo dos dados que contém no arquivo utilizando o [dicionário da base escolhida]([/Sprint%203/Desafio/googleplaystore.csv](https://dados.antt.gov.br/dataset/ef0171a8-f0df-4817-a4ed-b4ff94d87194/resource/e419a6ff-6f53-4f70-a7e1-5040a8d3c3ae/download/demostrativo_acidentes_dicionario_dados.pdf)) disponibilizado pela própria organização, para analisar os dados e verificar possíveis tratamentos.
- Percebi que a codificação estava em latin-1 e alguns dados estavam vindo incorretos por conta disso, então fiz a conversão para a codificação utf-8 utilizando o comando `incov` do linux, como exibido abaixo:

```
iconv -f ISO-8859-1 -t UTF-8 demostrativo_acidentes_riosp.csv > demostrativo_acidentes_riosp_utf8.csv
```
- Analisei também que o formato de data não estava no padrão correspondete ao tipo TIMESTAMP do s3 select, então fiz o tratamento da coluna de data utilizando o LibreOfficeCalc de DD/MM/AAAA para AAAA-MM-DD, como mostradado abaixo:
  <div style="text-align: center; padding: 10px;">
    <img src="/sprint5/Desafio/Evidencias/coluna-data-nao-formatada.png" width="100%" style="padding: 10px;">
  </div>
  <div style="text-align: center; padding: 10px;">
    <img src="/sprint5/Desafio/Evidencias/coluna-data-formatada.png" width="100%" style="padding: 10px;">
  </div>

## 3️⃣ Criação do bucket S3 na AWS e armazenamento da base de dados

- Após o tratamento dos dados, criei um bucket S3 com o nome `basededadossprint5` na aws e armazenei a base de dados no bucket
  <div style="text-align: center; padding: 10px;">
    <img src="/sprint5/Desafio/Evidencias/buckets3.png" width="100%" style="padding: 10px;">
  </div>

## 4️⃣ Configuração de acesso ao bucket s3

- Para conseguir extrair os dados do bucket, instalei a aws cli com o comando: 
```
sudo apt install awscli
```
- Com a cli da aws instalada configurei com as minhas chaves de acesso do usuário raiz utilizando `aws configure` e colando o token no terminal. Para verificar se estava conectado, rodei o comando `aws s3 ls` para listar os meus buckets.
  <div style="text-align: center; padding: 10px;">
    <img src="/sprint5/Desafio/Evidencias/listagemBucketsAwsCli.png" width="100%" style="padding: 10px;">
  </div>

## 5️⃣ Consulta proposta

- A consulta desejada na base de dados é: `Exibir o total de acidentes, total de vítimas ilesas, levemente feridas, moderamente feridas, gravemente feridas, fatalidades, soma total de envolvidos e uma frase com o arredodamento do total envolvídos registrados na BR-116 de São Paulo ao Rio de Janeiro durante o ano de 2023.`

## 6️⃣ Desenvolvimento do código em `python` para consulta utilizando o `S3 Select` através da biblioteca `boto3`

- Para conseguir realizar a consulta proposta e acessar localmente o bucket s3 basededadossprint5 que está a base de dados dos acidentes, desenvolvi um código em python utlizando a biblioteca boto3
- Instalação da biblioteca boto3:
  ```
  pip3 install boto3
  ``` 
- [Código em python](app/index.py) baseado na [documentação do s3 select da aws](https://aws.amazon.com/pt/blogs/storage/querying-data-without-servers-or-databases-using-amazon-s3-select/):
  ```
  import boto3

  s3 = boto3.client('s3')

  with open('app/queries-sql/quereS3Select.sql', 'r') as query:
      queryS3Select = query.read()

  response = s3.select_object_content(
      Bucket='basededadossprint5',
      Key='demostrativo_acidentes_riosp_formatado.csv',
      ExpressionType='SQL',
      Expression=queryS3Select,
      InputSerialization = {
          'CSV': {
              'FileHeaderInfo': 'USE', 
              'RecordDelimiter': '\n',
              'FieldDelimiter': ',',
              'QuoteCharacter': '"',        
          }
      },
      OutputSerialization = {'CSV': {}},
  )
  print('Total de acidentes, total de vítimas ilesas, levemente feridas, moderamente feridas, gravemente feridas, fatalidades, soma total de envolvidos, frase de arredodamento de total envolvídos')
  for event in response['Payload']:
      if 'Records' in event:
          records = event['Records']['Payload'].decode('utf-8')
          print(records)
      elif 'Stats' in event:
          statsDetails = event['Stats']['Details']
          print("Stats details bytesScanned: ")
          print(statsDetails['BytesScanned'])
          print("Stats details bytesProcessed: ")
          print(statsDetails['BytesProcessed'])
          print("Stats details bytesReturned: ")
          print(statsDetails['BytesReturned'])
  ```

- A consulta realizada adicionei no arquivo [quereS3Select.sql](app/queries-sql/quereS3Select.sql):
  ```
   SELECT
        COUNT(*),
        SUM(CAST(ilesos AS DECIMAL)),
        SUM(CAST(levemente_feridos AS DECIMAL)),
        SUM(CAST(moderadamente_feridos AS DECIMAL)),
        SUM(CAST(gravemente_feridos AS DECIMAL)),
        SUM(CAST(mortos AS DECIMAL)),
        SUM(CAST(mortos AS DECIMAL)+
            CAST(gravemente_feridos AS DECIMAL)+
            CAST(moderadamente_feridos AS DECIMAL)+
            CAST(levemente_feridos AS DECIMAL)+
            CAST(ilesos AS DECIMAL)),
        CASE WHEN 
            SUM(CAST(mortos AS DECIMAL)+
            CAST(gravemente_feridos AS DECIMAL)+
            CAST(moderadamente_feridos AS DECIMAL)+
            CAST(levemente_feridos AS DECIMAL)+
            CAST(ilesos AS DECIMAL))
         > 100000 THEN UPPER('mais de 100 mil vítimas') 
         WHEN
            SUM(CAST(mortos AS DECIMAL)+
            CAST(gravemente_feridos AS DECIMAL)+
            CAST(moderadamente_feridos AS DECIMAL)+
            CAST(levemente_feridos AS DECIMAL)+
            CAST(ilesos AS DECIMAL))
         > 50000 THEN UPPER('mais de 50 mil vitimas')
        WHEN
            SUM(CAST(mortos AS DECIMAL)+
            CAST(gravemente_feridos AS DECIMAL)+
            CAST(moderadamente_feridos AS DECIMAL)+
            CAST(levemente_feridos AS DECIMAL)+
            CAST(ilesos AS DECIMAL))
         > 20000 THEN UPPER('mais de 20 mil vitimas')
        WHEN
            SUM(CAST(mortos AS DECIMAL)+
            CAST(gravemente_feridos AS DECIMAL)+
            CAST(moderadamente_feridos AS DECIMAL)+
            CAST(levemente_feridos AS DECIMAL)+
            CAST(ilesos AS DECIMAL))
         > 10000 THEN UPPER('mais de 10 mil vitimas')
         WHEN
            SUM(CAST(mortos AS DECIMAL)+
            CAST(gravemente_feridos AS DECIMAL)+
            CAST(moderadamente_feridos AS DECIMAL)+
            CAST(levemente_feridos AS DECIMAL)+
            CAST(ilesos AS DECIMAL))
         > 5000 THEN UPPER('mais de 5 mil vitimas')
         WHEN
            SUM(CAST(mortos AS DECIMAL)+
            CAST(gravemente_feridos AS DECIMAL)+
            CAST(moderadamente_feridos AS DECIMAL)+
            CAST(levemente_feridos AS DECIMAL)+
            CAST(ilesos AS DECIMAL))
         > 1000 THEN UPPER('mais de mil vitimas')
         WHEN
            SUM(CAST(mortos AS DECIMAL)+
            CAST(gravemente_feridos AS DECIMAL)+
            CAST(moderadamente_feridos AS DECIMAL)+
            CAST(levemente_feridos AS DECIMAL)+
            CAST(ilesos AS DECIMAL))
         > 100 THEN UPPER('mais de 100 vitimas')
         ELSE UPPER('MENOS DE 100 VITIMAS') END 

    FROM s3object s 
        where EXTRACT(YEAR FROM CAST(data AS TIMESTAMP)) = 2023 
        and 
        (UPPER(s.trecho) = UPPER('BR-116/SP') or UPPER(s.trecho) = UPPER('BR-116/RJ'))
  ```

## 7️⃣ Detalhes da consulta

- Contagem da quantidade total de acidentes;
  - Utilizando a função de agregação `COUNT()`:
```
SELECT
    COUNT(*),
```
- Soma da quantidade de vítimas ilesas;
  - Utilizando a função de agregação `SUM()` e a função de conversão `CAST()` para o tipo DECIMAL(os tipos INT e INTEGER não funcionaram com a minha base de dados):
  ```
  SUM(CAST(ilesos AS DECIMAL)),
  ```
- Soma da quantidade de vítimas levemente feridas;
  - Utilizando a função de agregação `SUM()` e a função de conversão `CAST()` para o tipo DECIMAL:
  ```
        SUM(CAST(levemente_feridos AS DECIMAL)),
  ```
- Soma da quantidade de vítimas moderamente feridas;
  - Utilizando a função de agregação `SUM()` e a função de conversão `CAST()` para o tipo DECIMAL:
  ```
        SUM(CAST(moderadamente_feridos AS DECIMAL)),
  ```
- Soma da quantidade de vítimas gravemente feridas;
  - Utilizando a função de agregação `SUM()` e a função de conversão `CAST()` para o tipo DECIMAL:
  ```
        SUM(CAST(gravemente_feridos AS DECIMAL)),
  ```
- Soma da quantidade das fatalidades;
  - Utilizando a função de agregação `SUM()` e a função de conversão `CAST()` para o tipo DECIMAL:
  ```
        SUM(CAST(mortos AS DECIMAL)),
  ```
- Soma do total de vítimas;
  - Utilizando a função de agregação `SUM()`, adição e a função de conversão `CAST()` para o tipo DECIMAL:
```
SUM(CAST(mortos AS DECIMAL)+
            CAST(gravemente_feridos AS DECIMAL)+
            CAST(moderadamente_feridos AS DECIMAL)+
            CAST(levemente_feridos AS DECIMAL)+
            CAST(ilesos AS DECIMAL)),
```
- Função condicional para exibir frase com o número total de vítimas de forma arredondada;
  - Utilizando `CASE` e a função de string `UPPER()` para padronizar a resposta em caixa alta.
```
        CASE WHEN 
            SUM(CAST(mortos AS DECIMAL)+
            CAST(gravemente_feridos AS DECIMAL)+
            CAST(moderadamente_feridos AS DECIMAL)+
            CAST(levemente_feridos AS DECIMAL)+
            CAST(ilesos AS DECIMAL))
         > 100000 THEN UPPER('mais de 100 mil vítimas') 
         WHEN
            SUM(CAST(mortos AS DECIMAL)+
            CAST(gravemente_feridos AS DECIMAL)+
            CAST(moderadamente_feridos AS DECIMAL)+
            CAST(levemente_feridos AS DECIMAL)+
            CAST(ilesos AS DECIMAL))
         > 50000 THEN UPPER('mais de 50 mil vitimas')
        WHEN
            SUM(CAST(mortos AS DECIMAL)+
            CAST(gravemente_feridos AS DECIMAL)+
            CAST(moderadamente_feridos AS DECIMAL)+
            CAST(levemente_feridos AS DECIMAL)+
            CAST(ilesos AS DECIMAL))
         > 20000 THEN UPPER('mais de 20 mil vitimas')
        WHEN
            SUM(CAST(mortos AS DECIMAL)+
            CAST(gravemente_feridos AS DECIMAL)+
            CAST(moderadamente_feridos AS DECIMAL)+
            CAST(levemente_feridos AS DECIMAL)+
            CAST(ilesos AS DECIMAL))
         > 10000 THEN UPPER('mais de 10 mil vitimas')
         WHEN
            SUM(CAST(mortos AS DECIMAL)+
            CAST(gravemente_feridos AS DECIMAL)+
            CAST(moderadamente_feridos AS DECIMAL)+
            CAST(levemente_feridos AS DECIMAL)+
            CAST(ilesos AS DECIMAL))
         > 5000 THEN UPPER('mais de 5 mil vitimas')
         WHEN
            SUM(CAST(mortos AS DECIMAL)+
            CAST(gravemente_feridos AS DECIMAL)+
            CAST(moderadamente_feridos AS DECIMAL)+
            CAST(levemente_feridos AS DECIMAL)+
            CAST(ilesos AS DECIMAL))
         > 1000 THEN UPPER('mais de mil vitimas')
         WHEN
            SUM(CAST(mortos AS DECIMAL)+
            CAST(gravemente_feridos AS DECIMAL)+
            CAST(moderadamente_feridos AS DECIMAL)+
            CAST(levemente_feridos AS DECIMAL)+
            CAST(ilesos AS DECIMAL))
         > 100 THEN UPPER('mais de 100 vitimas')
         ELSE UPPER('MENOS DE 100 VITIMAS') END 
```
- Filtragem para pegar somente os acidentes registrados no ano de 2023 e na br 116 nos trechos do estado de São Paulo(SP) ou Rio de Janeiro(RJ)
  - Utilizando a função de data `EXTRACT()` para extrair somente o ano(year) da coluna data, em conjunto com a a função de conversão `CAST()` para a tipagem TIMESTAMP que é tipo do parametro da função extract;
  - Operadores lógicos `and` e `or`;
  - Função de string `UPPER()` para padronizar os dados da coluna trecho(alguns dados estavam em minúsculo e outros em maiúsculo) para realizar a comparação entre strings;
  ```
      FROM s3object s 
        where EXTRACT(YEAR FROM CAST(data AS TIMESTAMP)) = 2023 
        and 
        (UPPER(s.trecho) = UPPER('BR-116/SP')
        or 
        UPPER(s.trecho) = UPPER('BR-116/RJ'))
  ```
## 8️⃣ Compilando o código python

- Resultado no terminal:
  <div style="text-align: center; padding: 10px;">
    <img src="/sprint5/Desafio/Evidencias/codigoCompilado.png" width="100%" style="padding: 10px;">
  </div>

## 9️⃣ Referências 

- [Referência SQL para o Amazon S3 Select](https://docs.aws.amazon.com/pt_br/AmazonS3/latest/userguide/s3-select-sql-reference.html)

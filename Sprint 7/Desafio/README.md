# Sobre o desafio
- O desafio dessa sprint consiste na segunda etapa do desafio final que é a de ingestão de dados que não contém nos arquivos csv da ultima etapa.
- Esses dados devem ser requisitados da api TMDP e adicionado no meu bucket s3 onde estou armazenando os dados do desafio final.
  
# Tema Desafio final
- Ao analisar mais a fundo a API do TMDB conclui que poderia enriquecer mais a minha análise proposta, então decidi mudar o meu tema do desafio final para o que esta agora no meu [README principal](/README.md)

# 📋 Etapas

## 1️⃣ Decidir quais dados iria extrair do TMDB

-  Para conseguir dados adicionais que consigam responder as minhas questões, analisei bem a API TMDB para saber em qual método de requisição estava os dados que eu precisava, então escolhi os seguintes métodos com os campos que preciso de cada:
   -  Discover: popularity, id, vote_average, vote_count, genre_ids, title, release_date, poster_path (para caso eu ter o suporte de conseguir automatizar a busca de imagem do poster do filme) e original_language.
   -  Details: imdb_id, origin_country e budget.
   -  Credits: actoring e director.

- Para realizar a filtragem dos dados que quero solicitar e eliminar dados irrelevantes:
  - Filmes do genero crime e guerra apenas. 
  - Media de votos acima de 0.
  - Contagem de votos acima de 5 (analisei esse padrão nos arquivos CSV).
  - Orçamento acima de 0.
  - Espaço de tempo de 01/01/2012 a 31/12/2022.
## 2️⃣ Criando função Lambda no console AWS
- Para automação da extração dos dados da api em arquivos json, criei um função lambda no console da aws com o nome `ingestao-dados-do-tmdb-desafio-final` com tempo de execução em Python 3.9 e na arquitetura x86_64.
![](Evidencias/print_criando_funcao_lamda_ingestao-dados-do-tmdb-desafio-final.png)
## 3️⃣ Criando layer para a lambda

- Primeiramente, foi criado o arquivo [Dockefile](desafio-final-etapa-2/Dockerfile) abaixo ( aproveitei o do exercício anterior de layer) para rodar em bash no terminal a imagem amazonlinux:laters (versão mais recente) e instalando o python3, python3-pip, zip e atualizando as ferramentas:
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
- Comando para criar a imagem com o nome amazonlinux
  ```
  docker build -t amazonlinuxpython39 .
  ```
- Código no terminal para rodar o container em modo bash:
    ```
    docker run -it amazonlinuxpython39 bash
    ```
- Evidência da criação da imagem e rodando a imagem em modo bash:
  ![](Evidencias/print_terminal_criando_imagem_amazonlinux39_e_rodando_container.png)

- Após rodar a imagem em bash criei a estrutura de diretórios `~/layer_dir/python` e acessei o diretório com os seguintes comando:
  ```
  mkdir -p ~/layer_dir/python
  cd  ~/layer_dir/python
  ```
- Com a estrutura crianda instalei a biblioteca python requests dentro do diretório python usando pip install
  ```
  pip install requests -t .
  ```
    ![](Evidencias/print_criando_diretorios_e_instalando_lib_requests.png)
- Após a instalação executei os seguintes comandos para sair do diretório python e zipar com comando zip definindo o nome camada-requests.zip
  ```
  cd ..
  zip -r camada-requests.zip .
  ```
  ![](Evidencias/print_comprimindo_com_zip_diretorio_python_com_a_lib_requests.png)
- O seguinte passo foi saber o id do container para copiar de dentro do container docker o arquivo camada-requests.zip para o diretório local na minha máquina e após copiar o arquivo parei de rodar o container utilizado.
    ```
    docker ps -a 
    docker cp 07241bbff7b1:/root/layer_dir/camada-requests.zip ./
    docker stop 07241bbff7b1
    ```
    ![](Evidencias/print_copiando_arquivo_camada-requests_de_dentro_do_container.png)
- Após o arquivo com as bibliotecas copiado na minha máquina, armazenei o arquivo em um bucket s3 na aws que criei para anexar as camadas de layer que possam ser utilizadas no meu desafio final.
  ![](Evidencias/print_arquivo_zip_com_lib_requests_no_buckets3.png)
- O próximo passo foi criar um layer para a bilbioteca requests apontando para o arquivo no bucket mostrado acima com as configurações abaixo:
  ![](Evidencias/print_criando_layer_para_lib_requests.png)
- Com a camada criada, acesei a função lambda que estou utiliando e adicionei a camada RequestsLayer a ela.
  ![](Evidencias/print_adicionando_layer_RequestLayer_na_funcao_lambda.png)
## 4️⃣ Criando uma role para lambda

- Para permitir que a função Lambda crie diretórios e insira dados JSON no bucket S3 desafio-final-filmes-e-series-anderson-neves, fui ao IAM no console da AWS, selecionei a função Lambda e adicionei a permissão S3:PutObject.
- Arquivo Json para permitir o acesso:
    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:PutObject"
                ],
                "Resource": "arn:aws:s3:::desafio-final-filmes-e-series-anderson-neves/*"
            }
        ]
    }
    ```
    ![](Evidencias/print_criando_role_S3putObject_para_lambda.png)


## 5️⃣ Adicionando variável de ambiente na lambda
![](Evidencias/print_adicionando_variavel_de_ambiente.png)

## 6️⃣ Criando código python

- Defini variabeis globais para deixar o código mais maleavel, conseguindo alterar

- Bibliotecas utilizadas

    ```python
    import json
    import requests
    import boto3
    from datetime import datetime
    import os
    ```
- Resgatando a data atual de compilação da função e formtando mês e dia para terem dois dígitos.
    ```python
    request_year = datetime.now().year
    month_requisition = f'{datetime.now().month:02d}'
    day_requisition = f'{datetime.now().day:02d}'
    ```
- Inicializando o cliente S3 como boto3
    ```python
        s3 = boto3.client('s3')
    ```
-  Definindo o nome do bucket e caminho que os arquivos json vão ser armazenados.

    ```python
    bucket_name = 'desafio-final-filmes-e-series-anderson-neves'
    storage_path_s3 = f'Raw/TMDB/JSON/Movies/{request_year}/{month_requisition}/{day_requisition}/'
    ```
- Resgatando variável de ambiente (token da api TMDB)

    ```python
    access_token_auth = os.environ['ACCESS_TOKEN_AUTH']
    ```
- Definindo a URL base e os cabeçalhos correspondentes a API TMDB para realizar as requisições
    ```python
    discover_url = "https://api.themoviedb.org/3/discover/movie"
    movie_url = "https://api.themoviedb.org/3/movie/"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token_auth}"
    }
    ```
- Definindo o intervalo dos filmes que serão consultados por ano.

    ```python
    start_year = 2012
    final_year = 2022
    ```
- Definindo os gêneros dos filmes e seus respectivos IDs no TMDB que serão usados para consulta.
    ```python
    genres_ids = {
        "crime": "80",
        "war": "10752"
    }
    ```
- Defino os demais parâmetros para requisição solicitando apenas filmes com média acima de 0 e votos acima de cinco.

    ```python
    sort_by = "vote_average.desc"
    vote_average_gte = 0
    vote_count_gte = 5
    ```
- Variável global para somar o tamanho total dos arquivos em mega bytes.
    ```python
    total_size_of_jsons_mb = 0;
    ```
- Criei uma função parar remover os campos indesejáveis dos meus arquivos json e dessa forma diminuir o tamanho dos arquivos.
- Função `remove_unwanted_fields`:
    ```python
    def remove_unwanted_fields(items, fields_to_remove):
        for item in items:
            for field in fields_to_remove:
                item.pop(field, None)
    ```

- Criei uma função para salvar os dados resgatados da API TMDB em arquivos JSON com limite de 100 filmes por arquivo e armazená-los no S3 para o caminho desejado.
- Parâmetros da função, respectivamente: Categoria dos dados, ano de lançamento, os dados da requisição, nome do bucket s3 e o caminho onde os dados serão enviados
- O padrão em que os arquivos json serão nomeados será: `movie_<genero>_<ano>_part_<x>_<AAAAMMDD>.json`
- Função `save_data`:
    ```python
    def save_data(genre, year, data, bucket_s3_name, storage_path_s3):

        global total_size_of_jsons_mb
        part = 1

        while data:
            # Definindo nome do arquivo no padrão: movie_<genero>_<ano>_part_<x>_<AAAAMMDD>.json
            file_name = f'movie_{genre}_{year}_part_{part}_{request_year}{month_requisition}{day_requisition}.json'

            # Definindo local temporário onde será armazenado o arquivo transformado em json na cache da função lambda
            local_temporary_file_path = f'/tmp/{file_name}'
            
            # Gravando os primeiros 100 itens do json com adição de uma indetação igual a 4, calculando o tamanho total do arquivo salvo concatenando com o valor total dos arquivos gravados em mega bytes, e excluindo os 100 itens já gravados 
            with open(local_temporary_file_path, 'w') as json_file:
                json.dump(data[:100], json_file, indent=4)
            total_size_of_jsons_mb += os.path.getsize(local_temporary_file_path) / (1024 * 1024)
            data = data[100:]
            part += 1

            # Enviando o arquivo json gerado para o bucket s3 usando o client
            try:
                s3.upload_file(local_temporary_file_path, bucket_s3_name, storage_path_s3 + file_name)
                print(f'Arquivo {file_name} enviado para o bucket {bucket_s3_name}')
            except FileNotFoundError:
                print(f'O arquivo {file_name} não foi encontrado.')
    ```

- A função lamda_handle é resposável por realizar as requisições http para API TMDB através de loops que estão organizados um dentro do outro na seguinte ordem.:
    1. `for genre, genre_id in genres_ids.items()`: 
       - Loop para realizar as requisições por gênero (os quais estão presentes no array genres_ids). Quando esse loop se encerrar será impresso o tamanho total dos arquivos json em mega bytes enviados para o bucket.
    2. `for year in range(start_year, final_year + 1)`: 
        - Loop para fazer as requisições pelo intervalo de ano de lançamento proposto (start_year - final_year).
        - Dentro do loop, é definido o dicionário `params` em que vão conter os parâmetros para realização da requisição, e bem como, com filtros que quero, os quais foram definidos acima.
          - Obs.: utilizei os parâmetros `primary_release_date.gte` `primary_release_date.lte` para filtrar o ano que quero, pois o parâmetro `year` da api me retorna dados não correspondentes com o ano informado.
        - Dentro desse loop é definido um array vazio que armazenará os filmes já filtrados.
    3. `while continue_pagination`: 
       - Loop para realizar requisições em todas as páginas dos parâmetros definidos utilizando o método `Discover` da api. 
       -  Quando esse loop se encerrar, o array contedo todos os dados será ordenado de forma decrescente de acordo ao orçamento (budget) através de uma função lambda do python, 
       -  Após isso a função save_data será chamada para organizar os arquivos json e armazená-los no bucket s3, em que vão conter um genero em expecífico em um ano específico.
    4. `for movie in movie_data['results']`: 
        - Após receber os resultados solicitados na api será realizado um loop para percorrer cada resultado do json (no escopo results), recolhendo o id dos filmes e realizando uma requisição para cada filme, através do seu id, no Método `Details` para pegar os detalhes como: orçamento, imtb_id e o pais de origem, os quais o método Discover não retorna. 
        - Nesse mesmo loop, será realizado uma outra requisição com o método `Credits` para pegar o elenco(cast) de cada filme e a equipe(crew) para porteriomente filtrar apenas os 5 atores principais do filme e os diretores. E logo após, retirar campos indesejáveis com a função `remove_unwanted_fields()`. 
        - Ademais, será verificado se o filme possui um orçamento maior que 0, se possuir será adicionado ao array geral que está armazenando os dados dos filmes por gênero e ano separado. 
- O método `requests.get()` da biblioteca requests, foi utilizado para realizar as requisições, onde utilizo como parâmetro a url, o cabeçalho e os parâmetros da API que quero receber.
- Função `lambda_handle`:
   
    ```python
    def lambda_handler(event, context):

        # Definindo a variável global
        global total_size_of_jsons_mb;

        # Loop para fazer as resquisições por gênero
        for genre, genre_id in genres_ids.items():
            # Loop para fazer as requisições por ano do intervalo de ano proposto
            for year in range(start_year, final_year + 1):
                # Definindo os parâmetros com os filtros para realizar a requisição
                params = {
                    "include_adult": "false",
                    "include_video": "false",
                    "language": "en-US",
                    "primary_release_date.gte": f"{year}-01-01",
                    "primary_release_date.lte": f"{year}-12-31",
                    "sort_by": {sort_by},
                    "vote_average.gte": {vote_average_gte},
                    "vote_count.gte": {vote_count_gte},
                    "with_genres": genre_id,  
                    "page": 1 
                }
                
                # Lista para armazenar todos os dados das requisições
                all_movies_with_details = []
                continue_pagination = True

                # Loop para realizar requisição em todas as paginas
                while continue_pagination:
                    # Realizando a solicitação para a API Discover
                    response = requests.get(discover_url, headers=headers, params=params)
                    # Verificando se a solicitação foi bem-sucedida
                    if response.status_code == 200:
                        # Convertendo a resposta para JSON
                        movie_data = response.json()

                        # Loop para realizar resquest em details e credits do TMDB de cada filme para pegar o orçamento, pais de origem e os 5 atores principais e diretores de cada filme
                        for movie in movie_data['results']:
                            # Realizando request de detalhes dos filmes em cada filme
                            movie_id = movie['id']
                            movie_details_response = requests.get(f"{movie_url}{movie_id}", headers=headers)
                            # Realizando request de creditos dos filmes em cada filme
                            credits_response = requests.get(f"{movie_url}{movie_id}/credits", headers=headers)
                            # Verifica se as solicitações foram bem-sucedidas e converter em json os dados
                            if movie_details_response.status_code == 200 and credits_response.status_code == 200:
                                movie_details = movie_details_response.json()
                                credits = credits_response.json()
                                
                                # Filtrando apenas os 5 atores principais e os diretores       
                                actors = [
                                    # Loop para filtrar no elenco apenas os 5 atores de 'credits'
                                    member for member in credits.get('cast', [])
                                    if member['known_for_department'] == 'Acting'
                                ][:5]
                                directors = [
                                    # Loop para filtrar apenas os diretores de 'credits'
                                    member for member in credits.get('crew', [])
                                    if member['job'] == 'Director'
                                ]

                                # Removendo os campos indesejados de atores e diretores
                                fields_to_remove = ['known_for_department', 'profile_path', 'cast_id', 'credit_id', 'department', 'adult', 'original_name']
                                remove_unwanted_fields(actors, fields_to_remove)
                                remove_unwanted_fields(directors, fields_to_remove)

                                # Removendo os campos indesejados do filme
                                fields_to_remove_from_movie = ['adult', 'backdrop_path', 'original_title', 'overview', 'video']
                                remove_unwanted_fields([movie], fields_to_remove_from_movie)
                                
                                # Adicionando os campos de orçamento, imdb_id, pais de origem, 5 atores principais e diretores a lista filme do loop
                                movie['budget'] = movie_details.get('budget', 0)
                                movie['imdb_id'] = movie_details.get('imdb_id', '')
                                movie['origin_country'] = movie_details.get('origin_country', [])
                                movie['actors'] = actors
                                movie['directors'] = directors

                                # Adicionando para a lista do conjunto de todos os filmes apenas se o orçamento for maior que 0
                                if movie['budget'] > 0:
                                    all_movies_with_details.append(movie)
                            else:
                                print(f"Erro ao obter detalhes ou créditos do filme {movie_id}: {movie_details_response.status_code}, {credits_response.status_code}")

                        # Retornando a página atual já percorrida
                        print(f'Página {params["page"]} de {movie_data["total_pages"]}')

                        # Verificando se há mais páginas para recuperar, caso exista adiciona mais um ao parametro 'page' e entra em loop novamente para fazer requisição de novas páginas 
                        if params['page'] < movie_data['total_pages']:
                            params['page'] += 1
                        # Caso não exista, o loop é parado
                        else:
                            continue_pagination = False
                    else:
                        print(f"Erro na solicitação: {response.status_code}")
                        continue_pagination = False

                # Ordenando a lista com todos os filmes por ordem decrescente do orçamento
                all_movies_with_details = sorted(all_movies_with_details, key=lambda x: x['budget'], reverse=True)

                # Chamando função para armazenar os dados dos filmes em arquivos json para o ano e gênero atual
                save_data(genre, year, all_movies_with_details, bucket_name, storage_path_s3)

        print(f'Tamanho total dos arquivos carregados no bucket: {total_size_of_jsons_mb:.2f} MB')
    ```
- Código completo em: [desafio-final-etapa-2/ingestao-dados-do-tmdb-desafio-final.py](desafio-final-etapa-2/ingestao-dados-do-tmdb-desafio-final.py)
- Com alguns teste, percebi que a função iria copilar por completo numa média de de 8 a 12 minutos. Então, configurei para que o seu tempo de execução máximo fosse de 15 minutos (máximo permitido), mas mantive as outras configurações padrões:
![](Evidencias/print_aumentando_tempo_de_execucao_funcao_lambda.png)

## 7️⃣ Evidência da execução
- Console de teste da função: 
  ![](Evidencias/print_console_de_execucao_funcao_lambda_parte_1.png)
  ![](Evidencias/print_console_de_execucao_funcao_lambda_parte_2.png)
- ClouldWatch
  ![](Evidencias/print_clouldWatch_log_execucao_funcao_lambda_parte_1.png)
  ![](Evidencias/print_clouldWatch_log_execucao_funcao_lambda_parte_2.png)
- Bucket desafio-final-filmes-e-series-anderson-neves
  ![](Evidencias/print_diretorio_TMDB_criado_no_bucket_apos_execucao_da_funcao_lambda.png)
  ![](Evidencias/print_evidencia_de_arquivos_no_bucket_s3.png)
- Arquivo Json aberto
  ![](Evidencias/print_estrutura_arquivo_json_salvo_parte_1.png)
  ![](Evidencias/print_estrutura_arquivo_json_salvo_parte_2.png)

## 8️⃣ Criando cronograma
- Para que meus dados sejam atualizados semanalmente, decidi criar um cronograma no serviço da AWS EventBridge para execução da função lambda de ingestão dos dados do tmdb para toda sexta as 21:30 no fuso horário America/Bahia sem uma janela de tempo flexível.
- Evidência das configurações do cronograma:
  ![](Evidencias/print_criando_cronograma_especificando_detalhes.png)
  ![](Evidencias/print_criando_cronograma_especificando_detalhes_parte_2.png) 
- Selecionando a minha função de ingestão que deve ser executada:
  ![](Evidencias/print_criando_cronograma_selecionando_funcao_a_ser_executada.png)
- Politica para nova tentátiva (máximo de 3 vezes)
  ![](Evidencias/print_criando_cronograma_especificando_politica_nova_tentativa.png)
- Permissões para o cronograma (a política padrão do EventBrigde foi criada quando eu criei o cronograma pela primeira vez):
  ![](Evidencias/print_criando_cronograma_especificando_permissoes.png)
- Após criar o cronograma:
  ![](Evidencias/print_cronograma_criado.png)
  ![](Evidencias/print_cronograma_criado_destino.png)
  ![](Evidencias/print_cronograma_politica_de_nova_tentativa.png)

## 9️⃣ Referencias

- [Criação de uma EventBridge regra da Amazon que é executada de acordo com um cronograma](https://docs.aws.amazon.com/pt_br/eventbridge/latest/userguide/eb-create-rule-schedule.html)
- [Exemplos de políticas baseadas em identidade para o Amazon S3](https://docs.aws.amazon.com/pt_br/AmazonS3/latest/userguide/example-policies-s3.html)
